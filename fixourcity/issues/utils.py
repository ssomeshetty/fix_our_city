
from authorities.models import Authority
import logging

# Set up logging
logger = logging.getLogger(__name__)

KEYWORD_AUTHORITY_MAP = {
    # BBMP
    "pothole": "Bruhat_Bengaluru_Mahanagara_Palike",
    "bad road": "Bruhat_Bengaluru_Mahanagara_Palike",
    "road damaged": "Bruhat_Bengaluru_Mahanagara_Palike",
    "broken footpath": "Bruhat_Bengaluru_Mahanagara_Palike",
    "garbage": "Bruhat_Bengaluru_Mahanagara_Palike",
    "trash": "Bruhat_Bengaluru_Mahanagara_Palike",
    "waste": "Bruhat_Bengaluru_Mahanagara_Palike",
    "dustbin": "Bruhat_Bengaluru_Mahanagara_Palike",
    "overflowing bin": "Bruhat_Bengaluru_Mahanagara_Palike",
    "illegal dumping": "Bruhat_Bengaluru_Mahanagara_Palike",
    "public toilet": "Bruhat_Bengaluru_Mahanagara_Palike",
    "open drain": "Bruhat_Bengaluru_Mahanagara_Palike",
    "footpath": "Bruhat_Bengaluru_Mahanagara_Palike",
    "encroachment": "Bruhat_Bengaluru_Mahanagara_Palike",
    "construction debris": "Bruhat_Bengaluru_Mahanagara_Palike",
    
    # BESCOM
    "streetlight": "Bangalore_Electricity_Supply_Company_Limited",
    "no streetlight": "Bangalore_Electricity_Supply_Company_Limited",
    "light not working": "Bangalore_Electricity_Supply_Company_Limited",
    "flickering light": "Bangalore_Electricity_Supply_Company_Limited",
    "electric pole": "Bangalore_Electricity_Supply_Company_Limited",
    "power outage": "Bangalore_Electricity_Supply_Company_Limited",
    "electricity": "Bangalore_Electricity_Supply_Company_Limited",
    
    # BWSSB
    "sewage": "Bangalore_Water_Supply_and_Sewerage_Board",
    "manhole": "Bangalore_Water_Supply_and_Sewerage_Board",
    "dirty water": "Bangalore_Water_Supply_and_Sewerage_Board",
    "contaminated water": "Bangalore_Water_Supply_and_Sewerage_Board",
    "water leakage": "Bangalore_Water_Supply_and_Sewerage_Board",
    "pipe burst": "Bangalore_Water_Supply_and_Sewerage_Board",
    "sewer": "Bangalore_Water_Supply_and_Sewerage_Board",
    "blocked drain": "Bangalore_Water_Supply_and_Sewerage_Board",
    
    # BBMP Horticulture
    "tree fallen": "BBMP_Horticulture",
    "tree blocking": "BBMP_Horticulture",
    "tree branch": "BBMP_Horticulture",
    "tree cutting": "BBMP_Horticulture",
    "tree pruning": "BBMP_Horticulture",
    "park": "BBMP_Horticulture",
    "garden": "BBMP_Horticulture",
    "playground": "BBMP_Horticulture",
    "broken bench": "BBMP_Horticulture",
    "park light": "BBMP_Horticulture",
    
    # KSPCB
    "pollution": "Karnataka_State_Pollution_Control_Board",
    "noise pollution": "Karnataka_State_Pollution_Control_Board",
    "air pollution": "Karnataka_State_Pollution_Control_Board",
    "water pollution": "Karnataka_State_Pollution_Control_Board",
    "industrial waste": "Karnataka_State_Pollution_Control_Board",
    "chemical smell": "Karnataka_State_Pollution_Control_Board",
    "smoke": "Karnataka_State_Pollution_Control_Board",
    
    # KUWSDB
    "drainage": "Karnataka_Urban_Water_Supply_and_Drainage_Board",
    "open drainage": "Karnataka_Urban_Water_Supply_and_Drainage_Board",
    "clogged drain": "Karnataka_Urban_Water_Supply_and_Drainage_Board",
    "rural water": "Karnataka_Urban_Water_Supply_and_Drainage_Board",
    "storm water": "Karnataka_Urban_Water_Supply_and_Drainage_Board",
}

def detect_authority(title):
    """
    Detect the concerned authority based on keywords in the issue title.
    Returns the Authority object if found, None otherwise.
    """
    if not title:
        return None
        
    title_lower = title.lower()
    print(f"Detecting authority for title: {title_lower}")
    
    # Fetch all authorities first and create a dictionary for faster lookups
    # Include both underscore and space versions of names
    authority_dict = {}
    try:
        for auth in Authority.objects.all():
            # Map both underscore and space-replaced versions to the same authority
            authority_dict[auth.name] = auth
            authority_dict[auth.name.replace('_', ' ')] = auth
            authority_dict[auth.name.replace(' ', '_')] = auth
    except Exception as e:
        print(f"Error fetching authorities: {e}")
        return None
    
    print(f"Available authorities: {list(authority_dict.keys())}")
    
    # Check for keyword matches
    for keyword, authority_name in KEYWORD_AUTHORITY_MAP.items():
        if keyword in title_lower:
            print(f"Found keyword match: '{keyword}' -> '{authority_name}'")
            
            # Try different variations of the authority name
            for name_variant in [
                authority_name,
                authority_name.replace('_', ' '),
                authority_name.replace(' ', '_')
            ]:
                if name_variant in authority_dict:
                    return authority_dict[name_variant]
            
            print(f"Warning: Matched keyword '{keyword}' but authority '{authority_name}' not found in database")
    
    return None

def get_all_authorities():
    """Helper function to get all authorities for debugging"""
    return list(Authority.objects.all().values_list('name', flat=True))