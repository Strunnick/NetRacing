from utils.Vector2 import Vector2D
import math

# Provides base physics of car
class CarBase:
    def __init__(self):
        self.LookAt = Vector2D(0, 1)
        self.Mass = 1500 # Масса, кг
        self.Length = 2.6 # Колесная база, м
        self.Adhesion = 1.0 # Коэфф. сцепления колес с поверхностью
        self.SteeringAngle = 0 # Угол на который в данный момент повернуты передние колеса
        self.Throttle = 0 # Текущий коэфф мощности двигателя (от 0 до 1)
        self.EnginePower = 15500 #   Мощность двигателя, уе
        self.Breaks = False # Тормоз
        self.Pos = Vector2D(0.0,0.0) # Текущее положение центра автомобиля
        self.LookAt = Vector2D(0.0,1.0) # Текущее направление корпуса
        self.Velocity = Vector2D(0.0,0.0) # Текущее направление движения (скорость), м/с
        self.IsSliding = False # Скольжение
        self.SteeringSens = 5.0 # Чувствительность руля
        self.AirFriction = 0.05 # Трение воздуха
        self.BreaksFriction = 1.0 # Трение при торможении
        self.TireFriction = 0.3 # Трение повернутых передних колес

    def Update(self, throttle, steering, breaks, dt):
        # max steering angle
        maxAngle = 30 * self.LookAt.ToRadians # pi / 180
        # dump steering
        k = self.SteeringSens * dt
        s = self.SteeringAngle
        s = s * (1 - k) + steering * k
        self.SteeringAngle = self.ToDiapason(s, -maxAngle, maxAngle)
        self.Throttle = self.ToDiapason(throttle, -1, 1.0)
        self.Breaks = breaks

        # F = ma
        force = self.Throttle * self.EnginePower; # сила тяги
        self.Velocity += self.LookAt * (force * dt / self.Mass)
        # air friction
        self.Velocity -= self.Velocity * (self.AirFriction * dt)

        #tires friction
        friction = self.TireFriction * abs(self.SteeringAngle) # трение повернутых шин

        # breaks
        if (self.Breaks):
            friction = self.BreaksFriction

        self.Velocity -= self.Velocity.Projection(self.LookAt) * (friction * self.Adhesion * dt)
        # wheels position
        frontWheel = self.Pos + self.LookAt * (self.Length / 2)
        backWheel = self.Pos - self.LookAt * (self.Length / 2)
        backWheel = self.CalcWheelMoving(backWheel, self.LookAt,self.Velocity, dt)
        frontWheel = self.CalcWheelMoving(frontWheel, self.LookAt.RotateAngle(self.SteeringAngle), self.Velocity, dt)
        #print('backWheel = ', backWheel)
        #print('frontWheel = ', frontWheel)
        self.LookAt = (frontWheel - backWheel).Normalized() # new car orientation
        speed = self.Velocity.Length() # calc new velocity

        prev = self.Velocity
        self.Velocity = self.LookAt * speed
        self.Velocity = prev.moveTowards(self.Velocity, 0.5 * self.Adhesion)

        self.Pos = self.Pos + (self.Velocity * dt) # assign new pos

    def ToDiapason(self,val, _min, _max):
        if (val < _min): return _min
        if (val > _max): return _max
        return val

    def CalcWheelMoving(self, wheelPos, wheelDir, velocity, dt):
        # раскладываем скорости вдоль и поперек колеса
        Vt = velocity.Projection(wheelDir) # tangent component
        Vn = velocity.Sub(Vt) # normal component

        # смещение колеса
        moving = (Vt + self.Velocity) * 0.5 * dt # с учетом скольжения
        # moving = Vt * dt 3 # без учета скольжения

        return wheelPos + moving
