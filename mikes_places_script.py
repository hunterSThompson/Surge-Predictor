from googleplaces import GooglePlaces, types

API_Key = 'AIzaSyDrLrg-3rCSRqrFiqnINVpAUowbvmdMyrc'

google_places = GooglePlaces('AIzaSyDrLrg-3rCSRqrFiqnINVpAUowbvmdMyrc')

result = google_places.nearby_search(location = 'Boston, Massachusetts', 
		keyword= 'Bars', radius=2000)


