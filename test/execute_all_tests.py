import unittest

if __name__ == "__main__":
    # TestLoader 객체를 생성합니다.
    loader = unittest.TestLoader()

    # 현재 디렉토리에서 테스트를 찾습니다.
    start_dir = "."

    # discover 메소드를 사용하여 테스트를 찾고 실행합니다.
    suite = loader.discover(start_dir, pattern="*_test.py")

    # TextTestRunner 객체를 생성하고 run 메소드를 사용하여 테스트를 실행합니다.
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
