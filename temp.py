def bin(n1, r):
    dp = [1]
    for i in range(1, r + 1, 1):
        dp.append(((n1 - i + 1) * dp[i - 1]) / i)
    return dp[r]


n = int(input())
ans = 0
k = n
while 2 * k + 1 >= n:
    ans += bin(k + 1, n - k)
    k -= 1
print(int(ans))