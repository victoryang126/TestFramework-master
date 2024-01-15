class A:
    class B:
        class C:
            pass

    @classmethod
    def get_nested_classes(cls, current_class=None, level=1):
        if current_class is None:
            current_class = cls

        nested_classes = []
        for name, obj in current_class.__dict__.items():
            if isinstance(obj, type) and obj.__module__ == current_class.__module__:
                nested_classes.append(name)
                if level > 1:
                    nested_classes.extend(cls.get_nested_classes(obj, level - 1))
        return nested_classes

# 使用A的函数获取嵌套类的名称
nested_class_names = A.get_nested_classes(level=2)

# 打印嵌套类的名称
print(f"Nested classes in A: {', '.join(nested_class_names)}")
