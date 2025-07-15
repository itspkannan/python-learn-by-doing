import inspect
from collections.abc import Callable
from typing import Any


class Registry:
    _factories: dict[type, Callable[..., Any]] = {}
    _instances: dict[str, Any] = {}

    @classmethod
    def register(cls, interface: type, factory: Callable[..., Any] | None = None):
        if factory is None:

            def wrapper(func):
                cls._factories[interface] = func
                return func

            return wrapper
        cls._factories[interface] = factory

    @classmethod
    def resolve(cls, interface: type, **kwargs) -> Any:
        if interface not in cls._factories:
            raise ValueError(f"No factory registered for {interface.__name__}")

        factory = cls._factories[interface]
        sig = inspect.signature(factory)
        accepted_args = {name: kwargs[name] for name in sig.parameters if name in kwargs}

        try:
            return factory(**accepted_args)
        except TypeError as e:
            raise TypeError(
                f"[Registry Error] Failed to resolve {interface.__name__} "
                f"with arguments {accepted_args}. Check factory signature.\nOriginal error: {e!s}"
            )

    @classmethod
    def register_instance(cls, name: str, instance: Any):
        cls._instances[name] = instance

    @classmethod
    def deregister_instance(cls, name: str):
        cls._instances.pop(name, None)

    @classmethod
    def get_instance(cls, name: str) -> Any | None:
        return cls._instances.get(name)

    @classmethod
    def list_instances(cls) -> list[Any]:
        return list(cls._instances.values())
