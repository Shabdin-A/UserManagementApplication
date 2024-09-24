import functools
import datetime
import sqlite3
import time


def performance_logger(group_id):
    def performance_logger_decorator(main_function):
        @functools.wraps(main_function)
        def wrapper(*args, **kwargs):
            function_name = main_function.__name__
            call_datetime = datetime.datetime.now().isoformat()

            start = time.time()
            result = main_function(*args, **kwargs)
            stop = time.time()

            execution_time = stop - start

            with sqlite3.connect("UserManagementDB04-222.db") as connection:
                cursor = connection.cursor()
                cursor.execute(f"""
                INSERT INTO PerformanceLogger (
                                      function_name,
                                      execution_time,
                                      call_datetime,
                                      function_group_id
                                  )
                                  VALUES (
                                      '{function_name}',
                                      '{execution_time}',
                                      '{call_datetime}',
                                      {group_id}
                                  );""")
                connection.commit()

            return result

        return wrapper

    return performance_logger_decorator
