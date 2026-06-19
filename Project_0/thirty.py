def generate_series(n_terms):
    """Generate the series: 9,99,8,89,7,79,... for n_terms elements."""
    if n_terms <= 0:
        return []
    res = []
    k = 9
    while len(res) < n_terms and k >= 0:
        # first element: k
        res.append(k)
        if len(res) >= n_terms:
            break
        # second element: concatenation of k and 9 (e.g., 8 -> 89)
        res.append(int(f"{k}9"))
        k -= 1
    return res


if __name__ == "__main__":
    try:
        n = int(input("Enter number of terms: ").strip())
    except Exception:
        print("Invalid input")
    else:
        print(generate_series(n))
