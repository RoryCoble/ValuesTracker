from packages.ApiRequests import ApiRequests
from datetime import datetime, timedelta
from packages.UiSettings import SettingsState

response = ApiRequests(SettingsState.api_url).get_historical_values('ROJRY').json()
response2 = ApiRequests(SettingsState.api_url).get_historical_values('OSWAU').json()

