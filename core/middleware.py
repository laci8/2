from .models import VisitorLog
import user_agents
from django.contrib.gis.geoip2 import GeoIP2
from django.utils import timezone
import socket

class VisitorLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.geoip = None
        
        try:
            self.geoip = GeoIP2()  # Inizializza GeoIP2 una sola volta
        except:
            # Gestisci errori di configurazione GeoIP2
            pass

    def __call__(self, request):
        # Elabora la richiesta prima che la vista venga chiamata
        
        # Ottieni l'IP reale (considerando i proxy)
        ip = self.get_client_ip(request)
        
        # Analizza lo user agent
        user_agent_string = request.META.get('HTTP_USER_AGENT', '')
        ua = user_agents.parse(user_agent_string)
        
        # Prepara i dati per il log
        log_data = {
            'ip_address': ip,
            'user_agent': user_agent_string,
            'referrer': request.META.get('HTTP_REFERER'),
            'path': request.path,
            'is_authenticated': request.user.is_authenticated,
            'device_type': 'mobile' if ua.is_mobile else ('tablet' if ua.is_tablet else 'desktop'),
            'browser': ua.browser.family,
            'os': ua.os.family,
            'timestamp': timezone.now()
        }
        
        # Aggiungi geolocalizzazione se disponibile
        country = self.get_country_from_ip(ip)
        if country:
            log_data['country'] = country
        
        # Crea il log del visitatore
        VisitorLog.objects.create(**log_data)
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Ottiene l'IP reale del client anche dietro proxy"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def get_country_from_ip(self, ip):
        """Determina il paese dall'indirizzo IP usando GeoIP2"""
        if not ip or not self.geoip:
            return None
            
        try:
            # Restituisce solo il codice paese (es: 'IT' invece di 'Italy')
            return self.geoip.country(ip)['country_code']
        except (KeyError, socket.gaierror, ValueError):
            # Gestisci errori di geolocalizzazione
            return None