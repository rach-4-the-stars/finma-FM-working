import numpy as np
from scipy.stats import norm

def black_scholes_call(S0, K, T, r, sigma):
    """
    Black-Scholes formula for European call option.
    
    Don't worry about understanding this formula - just use it!
    """
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    call_price = S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

# TODO: Generate n_sims random numbers from standard normal distribution
def options(S0, K, T, r, sigma, n_sims):
    Z = np.random.randn(n_sims)

    print(f"Generated {len(Z)} random numbers")
    print(f"First 5 random numbers: {Z[:5]}")

    # TODO: Calculate the final stock prices
    # Step by step:
    # 1. Calculate drift = (r - 0.5 * sigma**2) * T
    # 2. Calculate diffusion = sigma * np.sqrt(T) * Z  
    # 3. Calculate ST = S0 * np.exp(drift + diffusion)

    drift = (r - 0.5 * sigma**2) * T
    diffusion = sigma * np.sqrt(T) * Z 
    ST = S0 * np.exp(drift + diffusion)

    print(f"Calculated {len(ST)} final stock prices")
    print(f"First 5 stock prices: {ST[:5]}")
    print(f"Min: ${ST.min():.2f}, Max: ${ST.max():.2f}, Mean: ${ST.mean():.2f}")

    # TODO: Calculate call option payoffs
    payoffs = np.maximum(ST - K, 0)


    print(f"Calculated {len(payoffs)} payoffs")
    print(f"First 10 payoffs: {payoffs[:10]}")
    print(f"Number of ITM options: {(payoffs > 0).sum()} out of {n_sims}")
    print(f"Average payoff: ${payoffs.mean():.4f}")

    #  TODO: Calculate the option price
    # 1. Calculate the average payoff
    # 2. Calculate the discount factor
    # 3. Multiply them together

    discount_factor = np.exp(-r * T)
    option_price = discount_factor * payoffs.mean()


    print(f"="*50)
    print(f"MONTE CARLO OPTION PRICING RESULT")
    print(f"="*50)
    print(f"Discount factor: {discount_factor:.6f}")
    print(f"Average payoff: ${payoffs.mean():.4f}")
    print(f"Option price: ${option_price:.4f}")
    print(f"="*50)
    print(f"Expected: ~$6.04")
    print(f"Your result: ${option_price:.4f}")
    print(f"Difference: ${abs(option_price - 6.04):.4f}")
    return option_price

def original_test():
    # Define parameters for our test
    S0 = 100      # Initial stock price
    K = 105       # Strike price
    T = 0.5       # Time to maturity (years)
    r = 0.05      # Risk-free rate
    sigma = 0.25  # Volatility
    n_sims = 10000  # Number of Monte Carlo simulations

    print(f"Parameters set!")
    print(f"S0={S0}, K={K}, T={T}, r={r}, sigma={sigma}")
    print(f"Number of simulations: {n_sims}")

    option_price = options(S0, K, T, r, sigma, n_sims)

    # Calculate Black-Scholes price
    bs_price = black_scholes_call(S0, K, T, r, sigma)

    # Our Monte Carlo price
    mc_price = option_price

    print(f"OPTION PRICING COMPARISON:")
    print(f"="*50)
    print(f"Black-Scholes (exact):  ${bs_price:.4f}")
    print(f"Monte Carlo (10,000):   ${mc_price:.4f}")
    print(f"="*50)
    print(f"Difference:             ${abs(bs_price - mc_price):.4f}")
    print(f"Error:                  {abs(bs_price - mc_price) / bs_price * 100:.2f}%")

    if abs(bs_price - mc_price) / bs_price < 0.02:  # Within 2%
        print(f"\n✓ Excellent! Monte Carlo matches Black-Scholes!")
    else:
        print(f"\n⚠ Try increasing number of simulations for better accuracy")


def exercise_2():
    # Define parameters for our test
    errors = {}
    for K in range(80,130, 10):
        S0 = 100      # Initial stock price
        T = 1       # Time to maturity (years)
        r = 0.05      # Risk-free rate
        sigma = 0.2  # Volatility
        n_sims = 10000  # Number of Monte Carlo simulations
        print(f"K={K}")
    

        option_price = options(S0, K, T, r, sigma, n_sims)

        # Calculate Black-Scholes price
        bs_price = black_scholes_call(S0, K, T, r, sigma)

        # Our Monte Carlo price
        mc_price = option_price

        print(f"OPTION PRICING COMPARISON:")
        print(f"="*50)
        print(f"Black-Scholes (exact):  ${bs_price:.4f}")
        print(f"Monte Carlo (10,000):   ${mc_price:.4f}")
        print(f"="*50)
        print(f"Difference:             ${abs(bs_price - mc_price):.4f}")
        print(f"Error:                  {abs(bs_price - mc_price) / bs_price * 100:.2f}%")

        if abs(bs_price - mc_price) / bs_price < 0.02:  # Within 2%
            print(f"\n✓ Excellent! Monte Carlo matches Black-Scholes!")
        else:
            print(f"\n⚠ Try increasing number of simulations for better accuracy")
        errors[K] = f"{abs(bs_price - mc_price) / bs_price * 100:.2f}%"

    for key in errors:
        print(f"K = {key} | Error = {errors[key]}")
if __name__ == "__main__":
    exercise_2()