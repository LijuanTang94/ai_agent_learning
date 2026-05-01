import sys

def fib(n):
    """返回第 n 个斐波那契数（F(0)=0, F(1)=1）"""
    if n < 0:
        raise ValueError("n 必须为非负整数")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("用法: python fib.py <n>")
        sys.exit(1)
    try:
        n = int(sys.argv[1])
        result = fib(n)
        print(result)
    except ValueError as e:
        print(f"错误: {e}")
        sys.exit(1)
