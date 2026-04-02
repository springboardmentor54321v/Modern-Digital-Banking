import requests
from datetime import datetime, timedelta

class CurrencyService:
    # Simple in-memory cache to prevent hitting the API limit too often
    _cache = {"rates": None, "last_updated": None}
    CACHE_DURATION = timedelta(hours=6)

    # MILESTONE 4 FALLBACK RATES (Used if API fails or Key is missing)
    FALLBACK_RATES = {
        "INR": 83.0,
        "EUR": 0.92,
        "GBP": 0.79,
        "USD": 1.0
    }

    @staticmethod
    def get_latest_rates():
        """Fetches exchange rates with simple 6-hour caching and fallback support."""
        now = datetime.utcnow()

        # 1. Return cached data if valid
        if CurrencyService._cache["rates"] and (now - CurrencyService._cache["last_updated"] < CurrencyService.CACHE_DURATION):
            return CurrencyService._cache["rates"]

        # 2. Attempt API Call
        API_KEY = "YOUR_FREE_KEY" 
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
        
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status() 
            data = response.json()
            rates = data.get("conversion_rates", {})
            
            # Extract only the currencies we support
            result = {
                "INR": rates.get("INR"),
                "EUR": rates.get("EUR"),
                "GBP": rates.get("GBP")
            }
            
            # Update cache if data is valid
            if result["INR"] is not None:
                CurrencyService._cache["rates"] = result
                CurrencyService._cache["last_updated"] = now
                return result
            
            # If data is missing from response, trigger fallback
            raise ValueError("Incomplete data from API")
            
        except Exception as e:
            # MILESTONE 4 LOGIC: Graceful degradation
            print(f"⚠️ DEBUG: Currency API Error ({e}). Using Milestone 4 Fallback Rates.")
            
            # Even if the API fails, we return valid numbers so the app keeps working
            return CurrencyService.FALLBACK_RATES

    @staticmethod
    def convert(amount: float, target_currency: str):
        """Converts an amount from USD to the target currency with high reliability."""
        rates = CurrencyService.get_latest_rates()
        
        # If rates is None or empty, something is wrong with the logic
        if not rates:
            return None
            
        rate = rates.get(target_currency.upper())
        
        # If the specific currency isn't found even in fallback, return None
        if rate is None:
            return None
            
        return round(amount * rate, 2)