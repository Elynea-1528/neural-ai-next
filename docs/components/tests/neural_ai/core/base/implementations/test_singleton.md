# 🧪 Teszt: tests/neural_ai/core/base/implementations/test_singleton.py

**Tesztelt modul:** [`neural_ai/core/base/implementations/singleton.py`](../../neural_ai/core/base/implementations/singleton.py)

SingletonMeta tesztelése.

Ez a modul tartalmazza a SingletonMeta metaclass egységtesztjeit,
beleértve a singleton minta ellenőrzését és a DI kompatibilitást.

## Teszt Osztály: `TestClass`

## Teszt Osztály: `ClassA`

## Teszt Osztály: `ClassB`

## Teszt Osztály: `TestClass`

## Teszt Osztály: `TestClass`

## Teszt Osztály: `TestClass`

## Teszt Osztály: `TestClass`

## Teszt Osztály: `BaseClass`

## Teszt Osztály: `TestClass`

## Teszt Osztály: `TestClass`

## Teszt Osztály: `TestClass`

## Teszt Osztály: `TestClass`

## Teszt Osztály: `TestSingletonMeta`

SingletonMeta metaclass tesztjei.

### ✓ `test_singleton_creates_only_one_instance()`

Teszteli, hogy csak egy példány jön létre.

## Teszt Függvények

### ✓ `test_singleton_different_classes()`

Teszteli, hogy különböző osztályok külön példányt kapnak.

### ✓ `test_singleton_with_kwargs()`

Teszteli a singleton-t kulcsszavas argumentumokkal.

### ✓ `test_singleton_without_args()`

Teszteli a singleton-t argumentumok nélkül.

### ✓ `test_singleton_has_initialized_flag()`

Teszteli, hogy a példánynak van _initialized flag-je (DI kompatibilitás).

### ✓ `test_singleton_has_instance_class_variable()`

Teszteli, hogy az osztálynak van _instance class változója (DI kompatibilitás).

### ✓ `test_singleton_multiple_inheritance()`

Teszteli a singleton-t többszörös öröklődés esetén.

### ✓ `test_singleton_with_class_method()`

Teszteli a singleton-t osztálymetódussal.

### ✓ `test_singleton_instances_dict()`

Teszteli, hogy a singleton tényleg egy példányt hoz létre.

### ✓ `test_singleton_reset_behavior()`

Teszteli, hogy a singleton nem enged második inicializálást.

---

**Teszt fájl:** [`tests/neural_ai/core/base/implementations/test_singleton.py`](../../tests/neural_ai/core/base/implementations/test_singleton.py)

**Tesztelt modul:** [`neural_ai/core/base/implementations/singleton.py`](../../neural_ai/core/base/implementations/singleton.py)
