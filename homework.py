from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = field(init=False)

    def __post_init__(self):
        self.message = (
            f"Тип тренировки: {self.training_type}; "
            f"Длительность: {self.duration:.3f} ч.; "
            f"Дистанция: {self.distance:.3f} км; "
            f"Ср. скорость: {self.speed:.3f} км/ч; "
            f"Потрачено ккал: {self.calories:.3f}.")

    def get_message(self) -> str:
        return self.message


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_HOUR: ClassVar[int] = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories(),
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_1, coeff_2 = 18., 20.
        return ((coeff_1 * self.get_mean_speed() - coeff_2)
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_HOUR)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_1, coeff_2 = 0.035, 0.029
        return ((coeff_1 + self.get_mean_speed() ** 2 // self.height * coeff_2)
                * self.weight * self.duration * self.MIN_IN_HOUR)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38

    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_1, coeff_2 = 1.1, 2.
        return (self.get_mean_speed() + coeff_1) * coeff_2 * self.weight


class WorkoutType:
    SWIMMING = "SWM"
    RUNNING = "RUN"
    SPORTS_WALKING = "WLK"


class TrainingFactory:
    WORKOUTS: Dict[str, Type[Training]] = {
        WorkoutType.SWIMMING: Swimming,
        WorkoutType.RUNNING: Running,
        WorkoutType.SPORTS_WALKING: SportsWalking,
    }

    @classmethod
    def create(cls, workout_type: str, *args: Any) -> Training:
        if workout_type not in cls.WORKOUTS:
            raise KeyError("Unknown workout type: '{workout_type}'")

        return cls.WORKOUTS[workout_type](*args)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    return TrainingFactory.create(workout_type, *data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        (WorkoutType.SWIMMING, [720, 1, 80, 25, 40]),
        (WorkoutType.RUNNING, [15000, 1, 75]),
        (WorkoutType.SPORTS_WALKING, [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
