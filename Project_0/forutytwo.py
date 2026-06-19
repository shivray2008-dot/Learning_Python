import numpy as np
import pandas as pd
import yfinance as yf
from scipy import stats
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Tuple, Dict, List
import warnings
warnings.filterwarnings('ignore')


@dataclass
class BusinessMetrics:
    """Fundamental business analytics scores"""
    profitability_score: float      # ROE, margins, earnings stability
    growth_score: float             # Revenue/earnings growth trends
    financial_health_score: float   # Debt ratios, current ratio, cash flow
    valuation_score: float          # P/E, P/B, PEG relative to sector
    momentum_score: float           # Price momentum, analyst revisions
    composite_score: float          # Weighted overall score


class StockAnalyzer:
    """
    Combines fundamental analysis with quantitative simulation.
    Uses business metrics to adjust drift and volatility parameters.
    """
    
    def __init__(self, ticker: str, lookback_years: int = 3):
        self.ticker = ticker.upper()
        self.lookback_years = lookback_years
        self.stock = yf.Ticker(self.ticker)
        self.hist = None
        self.returns = None
        self.metrics = None
        
    def fetch_data(self) -> pd.DataFrame:
        """Fetch historical price and fundamental data"""
        self.hist = self.stock.history(period=f"{self.lookback_years}y")
        if self.hist.empty:
            raise ValueError(f"No data found for {self.ticker}")
        
        self.returns = self.hist['Close'].pct_change().dropna()
        return self.hist
    
    # -------------------------------------------------------------------------
    # BUSINESS ANALYTICS MODULE
    # -------------------------------------------------------------------------
    
    def analyze_profitability(self) -> Tuple[float, Dict]:
        """Analyze profitability metrics (0-100 scale)"""
        info = self.stock.info
        details = {}
        
        # Return on Equity
        roe = info.get('returnOnEquity', 0) or 0
        details['ROE'] = f"{roe:.1%}" if roe else "N/A"
        roe_score = min(100, max(0, roe * 400))  # 25% ROE = 100
        
        # Profit Margins
        profit_margin = info.get('profitMargins', 0) or 0
        details['Profit Margin'] = f"{profit_margin:.1%}" if profit_margin else "N/A"
        margin_score = min(100, max(0, profit_margin * 500))  # 20% margin = 100
        
        # Operating Margins
        op_margin = info.get('operatingMargins', 0) or 0
        details['Operating Margin'] = f"{op_margin:.1%}" if op_margin else "N/A"
        op_score = min(100, max(0, op_margin * 400))
        
        # Earnings stability (lower volatility = better)
        if len(self.returns) > 60:
            earnings_vol = self.returns.rolling(60).std().mean()
            stability_score = max(0, 100 - earnings_vol * 2000)
        else:
            stability_score = 50
        details['Earnings Stability'] = f"{stability_score:.0f}/100"
        
        final_score = (roe_score * 0.35 + margin_score * 0.25 + 
                       op_score * 0.2 + stability_score * 0.2)
        
        return final_score, details
    
    def analyze_growth(self) -> Tuple[float, Dict]:
        """Analyze growth metrics (0-100 scale)"""
        info = self.stock.info
        details = {}
        
        # Revenue Growth
        rev_growth = info.get('revenueGrowth', 0) or 0
        details['Revenue Growth'] = f"{rev_growth:.1%}" if rev_growth else "N/A"
        rev_score = min(100, max(0, 50 + rev_growth * 200))
        
        # Earnings Growth
        earn_growth = info.get('earningsGrowth', 0) or 0
        details['Earnings Growth'] = f"{earn_growth:.1%}" if earn_growth else "N/A"
        earn_score = min(100, max(0, 50 + earn_growth * 150))
        
        # Historical price CAGR
        if len(self.hist) > 252:
            years = len(self.hist) / 252
            total_return = self.hist['Close'].iloc[-1] / self.hist['Close'].iloc[0]
            cagr = (total_return ** (1/years)) - 1
            details['Price CAGR'] = f"{cagr:.1%}"
            cagr_score = min(100, max(0, 50 + cagr * 300))
        else:
            cagr_score = 50
            details['Price CAGR'] = "N/A"
        
        final_score = rev_score * 0.35 + earn_score * 0.35 + cagr_score * 0.3
        return final_score, details
    
    def analyze_financial_health(self) -> Tuple[float, Dict]:
        """Analyze balance sheet health (0-100 scale)"""
        info = self.stock.info
        details = {}
        
        # Debt to Equity
        debt_equity = info.get('debtToEquity', 100) or 100
        details['Debt/Equity'] = f"{debt_equity:.1f}%" if debt_equity else "N/A"
        debt_score = max(0, 100 - debt_equity * 0.5)  # 0% D/E = 100, 200% = 0
        
        # Current Ratio
        current_ratio = info.get('currentRatio', 1) or 1
        details['Current Ratio'] = f"{current_ratio:.2f}"
        current_score = min(100, max(0, current_ratio * 40))  # 2.5 = 100
        
        # Free Cash Flow Yield
        fcf = info.get('freeCashflow', 0) or 0
        market_cap = info.get('marketCap', 1) or 1
        fcf_yield = fcf / market_cap if market_cap > 0 else 0
        details['FCF Yield'] = f"{fcf_yield:.1%}"
        fcf_score = min(100, max(0, fcf_yield * 1000))  # 10% FCF yield = 100
        
        final_score = debt_score * 0.4 + current_score * 0.3 + fcf_score * 0.3
        return final_score, details
    
    def analyze_valuation(self) -> Tuple[float, Dict]:
        """Analyze valuation metrics (0-100 scale, higher = more attractive)"""
        info = self.stock.info
        details = {}
        
        # Forward P/E (lower is better, but not too low)
        fwd_pe = info.get('forwardPE', 20) or 20
        details['Forward P/E'] = f"{fwd_pe:.1f}" if fwd_pe and fwd_pe > 0 else "N/A"
        if fwd_pe and fwd_pe > 0:
            pe_score = max(0, min(100, 120 - fwd_pe * 3))  # P/E 10 = 90, P/E 30 = 30
        else:
            pe_score = 50
        
        # PEG Ratio (closer to 1 is fair, <1 is attractive)
        peg = info.get('pegRatio', 1.5) or 1.5
        details['PEG Ratio'] = f"{peg:.2f}" if peg else "N/A"
        if peg and peg > 0:
            peg_score = max(0, min(100, 100 - (peg - 1) * 50))
        else:
            peg_score = 50
        
        # Price to Book
        pb = info.get('priceToBook', 3) or 3
        details['P/B Ratio'] = f"{pb:.2f}" if pb else "N/A"
        pb_score = max(0, min(100, 100 - pb * 15))
        
        final_score = pe_score * 0.4 + peg_score * 0.35 + pb_score * 0.25
        return final_score, details
    
    def analyze_momentum(self) -> Tuple[float, Dict]:
        """Analyze price momentum and technical factors (0-100 scale)"""
        details = {}
        
        if len(self.hist) < 200:
            return 50, {'Status': 'Insufficient data'}
        
        close = self.hist['Close']
        
        # 50-day vs 200-day MA (Golden/Death Cross signal)
        ma50 = close.rolling(50).mean().iloc[-1]
        ma200 = close.rolling(200).mean().iloc[-1]
        current_price = close.iloc[-1]
        
        ma_ratio = ma50 / ma200
        details['MA50/MA200'] = f"{ma_ratio:.3f}"
        ma_score = min(100, max(0, 50 + (ma_ratio - 1) * 200))
        
        # RSI (14-day)
        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs)).iloc[-1]
        details['RSI (14)'] = f"{rsi:.1f}"
        # RSI 30-70 is neutral zone, extremes are overbought/oversold
        rsi_score = 100 - abs(rsi - 50) * 2
        
        # Price vs 52-week range
        high_52w = close.tail(252).max()
        low_52w = close.tail(252).min()
        range_position = (current_price - low_52w) / (high_52w - low_52w)
        details['52W Range Position'] = f"{range_position:.1%}"
        range_score = range_position * 100
        
        final_score = ma_score * 0.4 + rsi_score * 0.3 + range_score * 0.3
        return final_score, details
    
    def compute_business_metrics(self) -> BusinessMetrics:
        """Compute all business analytics scores"""
        prof_score, prof_details = self.analyze_profitability()
        growth_score, growth_details = self.analyze_growth()
        health_score, health_details = self.analyze_financial_health()
        val_score, val_details = self.analyze_valuation()
        mom_score, mom_details = self.analyze_momentum()
        
        # Weighted composite
        weights = {
            'profitability': 0.25,
            'growth': 0.25,
            'financial_health': 0.20,
            'valuation': 0.15,
            'momentum': 0.15
        }
        
        composite = (prof_score * weights['profitability'] +
                     growth_score * weights['growth'] +
                     health_score * weights['financial_health'] +
                     val_score * weights['valuation'] +
                     mom_score * weights['momentum'])
        
        self.metrics = BusinessMetrics(
            profitability_score=prof_score,
            growth_score=growth_score,
            financial_health_score=health_score,
            valuation_score=val_score,
            momentum_score=mom_score,
            composite_score=composite
        )
        
        self._metric_details = {
            'Profitability': prof_details,
            'Growth': growth_details,
            'Financial Health': health_details,
            'Valuation': val_details,
            'Momentum': mom_details
        }
        
        return self.metrics
    
    # -------------------------------------------------------------------------
    # QUANTITATIVE SIMULATION MODULE
    # -------------------------------------------------------------------------
    
    def estimate_gbm_parameters(self) -> Tuple[float, float]:
        """
        Estimate drift (μ) and volatility (σ) for Geometric Brownian Motion.
        Adjusts parameters based on business analytics scores.
        """
        # Historical estimates
        annual_return = self.returns.mean() * 252
        annual_vol = self.returns.std() * np.sqrt(252)
        
        if self.metrics is None:
            self.compute_business_metrics()
        
        # Adjust drift based on composite score
        # Score 50 = neutral, >50 = bullish adjustment, <50 = bearish
        score_adjustment = (self.metrics.composite_score - 50) / 100
        adjusted_drift = annual_return + score_adjustment * 0.10  # ±10% max adjustment
        
        # Adjust volatility based on financial health (healthier = lower vol adjustment)
        health_factor = 1 - (self.metrics.financial_health_score - 50) / 200
        adjusted_vol = annual_vol * health_factor
        
        return adjusted_drift, max(0.05, adjusted_vol)  # Floor vol at 5%
    
    def run_monte_carlo(
        self,
        n_simulations: int = 100,
        forecast_days: int = 252,
        confidence_levels: List[float] = [0.05, 0.25, 0.50, 0.75, 0.95]
    ) -> Dict:
        """
        Run Monte Carlo simulation using Geometric Brownian Motion.
        
        GBM: dS = μS dt + σS dW
        Discrete: S(t+1) = S(t) * exp((μ - σ²/2)dt + σ√dt * Z)
        """
        if self.hist is None:
            self.fetch_data()
        
        mu, sigma = self.estimate_gbm_parameters()
        S0 = self.hist['Close'].iloc[-1]
        dt = 1/252  # Daily steps
        
        # Generate price paths
        np.random.seed(42)  # Reproducibility
        Z = np.random.standard_normal((n_simulations, forecast_days))
        
        # GBM simulation
        drift = (mu - 0.5 * sigma**2) * dt
        diffusion = sigma * np.sqrt(dt) * Z
        daily_returns = np.exp(drift + diffusion)
        
        price_paths = np.zeros((n_simulations, forecast_days + 1))
        price_paths[:, 0] = S0
        
        for t in range(1, forecast_days + 1):
            price_paths[:, t] = price_paths[:, t-1] * daily_returns[:, t-1]
        
        # Calculate statistics
        final_prices = price_paths[:, -1]
        
        results = {
            'price_paths': price_paths,
            'initial_price': S0,
            'forecast_days': forecast_days,
            'n_simulations': n_simulations,
            'drift': mu,
            'volatility': sigma,
            'final_prices': {
                'mean': np.mean(final_prices),
                'median': np.median(final_prices),
                'std': np.std(final_prices),
                'min': np.min(final_prices),
                'max': np.max(final_prices)
            },
            'percentiles': {
                f'p{int(p*100)}': np.percentile(final_prices, p*100) 
                for p in confidence_levels
            },
            'returns': {
                'mean': (np.mean(final_prices) / S0 - 1),
                'median': (np.median(final_prices) / S0 - 1),
                'prob_positive': np.mean(final_prices > S0),
                'prob_10pct_gain': np.mean(final_prices > S0 * 1.10),
                'prob_10pct_loss': np.mean(final_prices < S0 * 0.90)
            }
        }
        
        return results
    
    def generate_report(self, simulation_results: Dict) -> str:
        """Generate a comprehensive analysis report"""
        info = self.stock.info
        company_name = info.get('shortName', self.ticker)
        
        report = []
        report.append("=" * 70)
        report.append(f"STOCK ANALYSIS REPORT: {company_name} ({self.ticker})")
        report.append("=" * 70)
        
        # Company Overview
        report.append(f"\n{'─' * 35}")
        report.append("COMPANY OVERVIEW")
        report.append(f"{'─' * 35}")
        report.append(f"Sector: {info.get('sector', 'N/A')}")
        report.append(f"Industry: {info.get('industry', 'N/A')}")
        report.append(f"Market Cap: ${info.get('marketCap', 0)/1e9:.2f}B")
        report.append(f"Current Price: ${self.hist['Close'].iloc[-1]:.2f}")
        
        # Business Analytics Scores
        report.append(f"\n{'─' * 35}")
        report.append("BUSINESS ANALYTICS SCORES (0-100)")
        report.append(f"{'─' * 35}")
        report.append(f"  Profitability:     {self.metrics.profitability_score:5.1f}")
        report.append(f"  Growth:            {self.metrics.growth_score:5.1f}")
        report.append(f"  Financial Health:  {self.metrics.financial_health_score:5.1f}")
        report.append(f"  Valuation:         {self.metrics.valuation_score:5.1f}")
        report.append(f"  Momentum:          {self.metrics.momentum_score:5.1f}")
        report.append(f"  {'─' * 25}")
        report.append(f"  COMPOSITE SCORE:   {self.metrics.composite_score:5.1f}")
        
        # Detailed Metrics
        report.append(f"\n{'─' * 35}")
        report.append("DETAILED METRICS")
        report.append(f"{'─' * 35}")
        for category, details in self._metric_details.items():
            report.append(f"\n  {category}:")
            for metric, value in details.items():
                report.append(f"    • {metric}: {value}")
        
        # Simulation Parameters
        report.append(f"\n{'─' * 35}")
        report.append("SIMULATION PARAMETERS")
        report.append(f"{'─' * 35}")
        report.append(f"  Adjusted Annual Drift (μ): {simulation_results['drift']:.2%}")
        report.append(f"  Adjusted Annual Volatility (σ): {simulation_results['volatility']:.2%}")
        report.append(f"  Simulations: {simulation_results['n_simulations']}")
        report.append(f"  Forecast Horizon: {simulation_results['forecast_days']} trading days")
        
        # Simulation Results
        report.append(f"\n{'─' * 35}")
        report.append("PRICE FORECAST RESULTS")
        report.append(f"{'─' * 35}")
        fp = simulation_results['final_prices']
        S0 = simulation_results['initial_price']
        
        report.append(f"  Starting Price: ${S0:.2f}")
        report.append(f"\n  Final Price Distribution:")
        report.append(f"    Mean:   ${fp['mean']:.2f} ({(fp['mean']/S0-1)*100:+.1f}%)")
        report.append(f"    Median: ${fp['median']:.2f} ({(fp['median']/S0-1)*100:+.1f}%)")
        report.append(f"    Std Dev: ${fp['std']:.2f}")
        report.append(f"    Range:  ${fp['min']:.2f} - ${fp['max']:.2f}")
        
        report.append(f"\n  Confidence Intervals:")
        pct = simulation_results['percentiles']
        report.append(f"    5th percentile:  ${pct['p5']:.2f} ({(pct['p5']/S0-1)*100:+.1f}%)")
        report.append(f"    25th percentile: ${pct['p25']:.2f} ({(pct['p25']/S0-1)*100:+.1f}%)")
        report.append(f"    50th percentile: ${pct['p50']:.2f} ({(pct['p50']/S0-1)*100:+.1f}%)")
        report.append(f"    75th percentile: ${pct['p75']:.2f} ({(pct['p75']/S0-1)*100:+.1f}%)")
        report.append(f"    95th percentile: ${pct['p95']:.2f} ({(pct['p95']/S0-1)*100:+.1f}%)")
        
        # Probability Analysis
        report.append(f"\n{'─' * 35}")
        report.append("PROBABILITY ANALYSIS")
        report.append(f"{'─' * 35}")
        ret = simulation_results['returns']
        report.append(f"  Probability of positive return: {ret['prob_positive']:.1%}")
        report.append(f"  Probability of >10% gain:       {ret['prob_10pct_gain']:.1%}")
        report.append(f"  Probability of >10% loss:       {ret['prob_10pct_loss']:.1%}")
        
        # Risk Assessment
        report.append(f"\n{'─' * 35}")
        report.append("RISK ASSESSMENT")
        report.append(f"{'─' * 35}")
        var_95 = S0 - pct['p5']
        report.append(f"  Value at Risk (95%): ${var_95:.2f} ({var_95/S0*100:.1f}% of portfolio)")
        report.append(f"  Expected Shortfall: ${S0 - np.mean(simulation_results['price_paths'][:,-1][simulation_results['price_paths'][:,-1] < pct['p5']]):.2f}")
        
        # Interpretation
        report.append(f"\n{'─' * 35}")
        report.append("INTERPRETATION")
        report.append(f"{'─' * 35}")
        
        composite = self.metrics.composite_score
        if composite >= 70:
            outlook = "BULLISH - Strong fundamentals support positive outlook"
        elif composite >= 55:
            outlook = "MODERATELY BULLISH - Solid metrics with some concerns"
        elif composite >= 45:
            outlook = "NEUTRAL - Mixed signals warrant caution"
        elif composite >= 30:
            outlook = "MODERATELY BEARISH - Several concerning metrics"
        else:
            outlook = "BEARISH - Significant fundamental weaknesses"
        
        report.append(f"  Overall Outlook: {outlook}")
        report.append(f"\n  Key Strengths:")
        scores = [
            ('Profitability', self.metrics.profitability_score),
            ('Growth', self.metrics.growth_score),
            ('Financial Health', self.metrics.financial_health_score),
            ('Valuation', self.metrics.valuation_score),
            ('Momentum', self.metrics.momentum_score)
        ]
        for name, score in sorted(scores, key=lambda x: -x[1])[:2]:
            report.append(f"    • {name}: {score:.1f}/100")
        
        report.append(f"\n  Key Concerns:")
        for name, score in sorted(scores, key=lambda x: x[1])[:2]:
            report.append(f"    • {name}: {score:.1f}/100")
        
        report.append("\n" + "=" * 70)
        report.append("DISCLAIMER: This analysis is for educational purposes only.")
        report.append("Past performance does not guarantee future results.")
        report.append("Always consult a financial advisor before investing.")
        report.append("=" * 70)
        
        return "\n".join(report)
    
    def plot_results(self, simulation_results: Dict):
        """Visualize simulation results"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        paths = simulation_results['price_paths']
        S0 = simulation_results['initial_price']
        final_prices = paths[:, -1]
        
        # 1. Price Paths
        ax1 = axes[0, 0]
        for i in range(min(100, paths.shape[0])):
            alpha = 0.3 if paths.shape[0] > 20 else 0.6
            ax1.plot(paths[i], alpha=alpha, linewidth=0.5)
        
        ax1.axhline(y=S0, color='black', linestyle='--', label='Starting Price')
        ax1.plot(np.median(paths, axis=0), color='red', linewidth=2, label='Median Path')
        ax1.fill_between(
            range(paths.shape[1]),
            np.percentile(paths, 5, axis=0),
            np.percentile(paths, 95, axis=0),
            alpha=0.2, color='blue', label='90% CI'
        )
        ax1.set_title(f'{self.ticker} - 100 Monte Carlo Price Paths', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Trading Days')
        ax1.set_ylabel('Price ($)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Final Price Distribution
        ax2 = axes[0, 1]
        ax2.hist(final_prices, bins=30, edgecolor='black', alpha=0.7, density=True)
        ax2.axvline(S0, color='black', linestyle='--', linewidth=2, label=f'Start: ${S0:.2f}')
        ax2.axvline(np.mean(final_prices), color='red', linestyle='-', linewidth=2, 
                    label=f'Mean: ${np.mean(final_prices):.2f}')
        ax2.axvline(np.median(final_prices), color='green', linestyle='-', linewidth=2,
                    label=f'Median: ${np.median(final_prices):.2f}')
        ax2.set_title('Final Price Distribution', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Price ($)')
        ax2.set_ylabel('Density')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Business Analytics Radar Chart
        ax3 = axes[1, 0]
        categories = ['Profitability', 'Growth', 'Financial\nHealth', 'Valuation', 'Momentum']
        values = [
            self.metrics.profitability_score,
            self.metrics.growth_score,
            self.metrics.financial_health_score,
            self.metrics.valuation_score,
            self.metrics.momentum_score
        ]
        
        # Create bar chart instead of radar for simplicity
        colors = ['#2ecc71' if v >= 60 else '#f39c12' if v >= 40 else '#e74c3c' for v in values]
        bars = ax3.barh(categories, values, color=colors, edgecolor='black')
        ax3.axvline(x=50, color='gray', linestyle='--', alpha=0.7)
        ax3.set_xlim(0, 100)
        ax3.set_title('Business Analytics Scores', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Score (0-100)')
        
        # Add score labels
        for bar, val in zip(bars, values):
            ax3.text(val + 2, bar.get_y() + bar.get_height()/2, f'{val:.0f}', 
                    va='center', fontsize=10)
        
        # 4. Return Distribution
        ax4 = axes[1, 1]
        returns = (final_prices / S0 - 1) * 100
        ax4.hist(returns, bins=30, edgecolor='black', alpha=0.7, 
                color=['green' if r > 0 else 'red' for r in sorted(returns)])
        ax4.axvline(0, color='black', linestyle='-', linewidth=2)
        ax4.axvline(np.mean(returns), color='blue', linestyle='--', linewidth=2,
                   label=f'Mean: {np.mean(returns):+.1f}%')
        ax4.set_title('Return Distribution', fontsize=12, fontweight='bold')
        ax4.set_xlabel('Return (%)')
        ax4.set_ylabel('Frequency')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.suptitle(f'{self.ticker} Stock Analysis & Monte Carlo Simulation', 
                    fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(f'{self.ticker}_analysis.png', dpi=150, bbox_inches='tight')
        plt.show()
        
        return fig


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def analyze_stock(ticker: str, forecast_days: int = 252, n_simulations: int = 100):
    """
    Main function to run complete stock analysis.
    
    Args:
        ticker: Stock symbol (e.g., 'AAPL', 'MSFT', 'GOOGL')
        forecast_days: Number of trading days to forecast (252 ≈ 1 year)
        n_simulations: Number of Monte Carlo paths to generate
    """
    print(f"\n🔍 Analyzing {ticker}...\n")
    
    # Initialize analyzer
    analyzer = StockAnalyzer(ticker, lookback_years=3)
    
    # Fetch data
    print("📊 Fetching historical data...")
    analyzer.fetch_data()
    
    # Compute business metrics
    print("📈 Computing business analytics...")
    analyzer.compute_business_metrics()
    
    # Run Monte Carlo simulation
    print(f"🎲 Running {n_simulations} Monte Carlo simulations...")
    results = analyzer.run_monte_carlo(
        n_simulations=n_simulations,
        forecast_days=forecast_days
    )
    
    # Generate and print report
    report = analyzer.generate_report(results)
    print(report)
    
    # Plot results
    print("\n📉 Generating visualizations...")
    analyzer.plot_results(results)
    
    return analyzer, results


# Run analysis
if __name__ == "__main__":
    # Example usage - change ticker as needed
    TICKER = "AAPL"  # Apple Inc.
    
    analyzer, results = analyze_stock(
        ticker=TICKER,
        forecast_days=252,    # 1 year forecast
        n_simulations=100     # 100 price paths
    )
