import inspect
from collections.abc import Callable
from typing import Any, Type, TypeVar

T = TypeVar("T")

class Registry:
    _factories: dict[Type, Callable[..., Any]] = {}
    _instances: dict[Any, Any] = {}

    @classmethod
    def register(cls, interface: Type[T], factory: Callable[..., T] | None = None):
        if factory is None:
            def wrapper(func: Callable[..., T]):
                cls._factories[interface] = func
                return func
            return wrapper
        cls._factories[interface] = factory

    @classmethod
    def resolve(cls, interface: Type[T], **kwargs) -> T:
        # 1. Return existing instance if available
        if interface in cls._instances:
            return cls._instances[interface]

        # 2. Build from factory if registered
        if interface not in cls._factories:
            raise ValueError(f"No factory registered for {interface.__name__}")

        factory = cls._factories[interface]
        sig = inspect.signature(factory)
        accepted_args = {name: kwargs[name] for name in sig.parameters if name in kwargs}

        try:
            instance = factory(**accepted_args)
            cls._instances[interface] = instance
            return instance
        except TypeError as e:
            raise TypeError(
                f"[Registry Error] Failed to resolve {interface.__name__} "
                f"with arguments {accepted_args}. Check factory signature.\nOriginal error: {e!s}"
            )

    @classmethod
    def register_instance(cls, key: str | Type, instance: Any):
        cls._instances[key] = instance

    @classmethod
    def deregister_instance(cls, key: str | Type):
        cls._instances.pop(key, None)

    @classmethod
    def get_instance(cls, key: str | Type) -> Any | None:
        return cls._instances.get(key)

    @classmethod
    def list_instances(cls) -> list[Any]:
        return list(cls._instances.values())
