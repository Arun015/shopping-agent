from langchain_core.tools import tool
from typing import List, Optional, Union
import logging
import json
import os
from backend.dao import phone_dao

logger = logging.getLogger(__name__)


@tool
def search_phones(
    budget_min: Optional[int] = None,
    budget_max: Optional[int] = None,
    brand: Optional[str] = None,
    features: Optional[Union[str, List[str]]] = None,
    min_camera_mp: Optional[int] = None,
    min_battery_mah: Optional[int] = None,
    sort_by: str = "price"
) -> str:
    """Search for mobile phones based on criteria.
    
    Args:
        budget_min: Minimum price in INR
        budget_max: Maximum price in INR
        brand: Brand name (Samsung, OnePlus, Xiaomi, etc.)
        features: List of required features (5G, OIS, IP68, etc.)
        min_camera_mp: Minimum camera megapixels
        min_battery_mah: Minimum battery capacity in mAh
        sort_by: Sort results by 'price', 'camera', 'battery', or 'performance'
    
    Returns:
        JSON string with matching phones including display size, specs, and features
    """
    # Normalize features to list format
    if features and isinstance(features, str):
        features = [features]
    
    results = phone_dao.search(
        budget_min=budget_min,
        budget_max=budget_max,
        brand=brand,
        features=features,
        min_camera_mp=min_camera_mp,
        min_battery_mah=min_battery_mah
    )
    
    results = phone_dao.sort_phones(results, sort_by)
    
    if not results:
        return "No phones found matching the criteria."
    
    results = results[:5]
    
    phones_data = []
    for phone in results:
        phones_data.append({
            "id": phone.id,
            "brand": phone.brand,
            "model": phone.model,
            "price": phone.price,
            "display_inches": phone.specs.display_inches,
            "camera_mp": phone.specs.camera.main_mp,
            "battery_mah": phone.specs.battery_mah,
            "processor": phone.specs.processor,
            "ram_gb": phone.specs.ram_gb,
            "storage_gb": phone.specs.storage_gb,
            "features": phone.features,
            "pros": phone.pros,
            "cons": phone.cons
        })
    
    return json.dumps(phones_data, indent=2)


@tool
def compare_phones(phone_models: List[str]) -> str:
    """Compare 2-3 mobile phones side by side.
    
    Args:
        phone_models: List of phone model names to compare (e.g., ["Pixel 8a", "OnePlus 12R"])
    
    Returns:
        JSON string with detailed comparison
    """
    if len(phone_models) < 2 or len(phone_models) > 3:
        return "Please provide 2-3 phone models to compare."
    
    phones = []
    for model in phone_models:
        phone = phone_dao.get_by_model(model)
        if phone:
            phones.append(phone)
    
    if len(phones) < 2:
        return f"Could not find all requested phones. Found: {[p.model for p in phones]}"
    
    comparison = {
        "phones": []
    }
    
    for phone in phones:
        comparison["phones"].append({
            "brand": phone.brand,
            "model": phone.model,
            "price": phone.price,
            "camera": {
                "main_mp": phone.specs.camera.main_mp,
                "features": phone.specs.camera.features
            },
            "battery_mah": phone.specs.battery_mah,
            "fast_charging_w": phone.specs.fast_charging_w,
            "processor": phone.specs.processor,
            "ram_gb": phone.specs.ram_gb,
            "storage_gb": phone.specs.storage_gb,
            "display_inches": phone.specs.display_inches,
            "refresh_rate_hz": phone.specs.refresh_rate_hz,
            "weight_g": phone.specs.weight_g,
            "features": phone.features,
            "pros": phone.pros,
            "cons": phone.cons
        })
    
    return json.dumps(comparison, indent=2)


@tool
def get_phone_details(phone_model: str) -> str:
    """Get detailed specifications of a specific phone.
    
    Args:
        phone_model: Phone model name or brand + model
    
    Returns:
        JSON string with complete phone details
    """
    phone = phone_dao.get_by_model(phone_model)
    
    if not phone:
        return f"Phone '{phone_model}' not found in database."
    
    details = {
        "brand": phone.brand,
        "model": phone.model,
        "price": phone.price,
        "specs": {
            "camera": {
                "main_mp": phone.specs.camera.main_mp,
                "ultrawide_mp": phone.specs.camera.ultrawide_mp,
                "macro_mp": phone.specs.camera.macro_mp,
                "features": phone.specs.camera.features
            },
            "battery_mah": phone.specs.battery_mah,
            "fast_charging_w": phone.specs.fast_charging_w,
            "processor": phone.specs.processor,
            "ram_gb": phone.specs.ram_gb,
            "storage_gb": phone.specs.storage_gb,
            "display_inches": phone.specs.display_inches,
            "refresh_rate_hz": phone.specs.refresh_rate_hz,
            "weight_g": phone.specs.weight_g
        },
        "features": phone.features,
        "pros": phone.pros,
        "cons": phone.cons
    }
    
    return json.dumps(details, indent=2)


def _load_technical_terms():
    """Load technical terms from database file"""
    terms_file = os.path.join(os.path.dirname(__file__), '../data/technical_terms.json')
    
    try:
        with open(terms_file, 'r') as f:
            terms_data = json.load(f)
        
        # Create lookup dictionary
        terms_dict = {}
        for term_info in terms_data:
            term_key = term_info['term'].lower()
            terms_dict[term_key] = term_info
            # Also add full name as key
            if term_info.get('full_name'):
                terms_dict[term_info['full_name'].lower()] = term_info
        
        return terms_dict
    except Exception as e:
        logger.error(f"Error loading technical terms: {e}", exc_info=True)
        return {}


def _get_phones_with_feature(feature: str):
    """Get phones from database that have a specific feature"""
    all_phones = phone_dao.get_all()
    matching_phones = []
    
    feature_lower = feature.lower()
    
    for phone in all_phones:
        # Check in features
        if any(feature_lower in f.lower() for f in phone.features):
            matching_phones.append(f"{phone.brand} {phone.model}")
        # Check in camera features
        elif any(feature_lower in cf.lower() for cf in phone.specs.camera.features):
            matching_phones.append(f"{phone.brand} {phone.model}")
    
    return matching_phones[:5]  # Return max 5 examples


@tool
def explain_technical_term(term: str) -> str:
    """Explain technical terms related to mobile phones using our technical terms database.
    Can also compare two terms when asked "X vs Y".
    
    Args:
        term: Technical term to explain (OIS, 5G, AMOLED, etc.) or comparison query (e.g., "OIS vs EIS")
    
    Returns:
        Detailed explanation from database with real phone examples
    """
    term_lower = term.lower().strip()
    
    # Load technical terms from database
    terms_db = _load_technical_terms()
    
    # Handle comparison queries (e.g., "OIS vs EIS", "AMOLED vs LCD")
    if " vs " in term_lower or " versus " in term_lower:
        separator = " vs " if " vs " in term_lower else " versus "
        terms = [t.strip() for t in term_lower.split(separator)]
        
        if len(terms) == 2:
            term1, term2 = terms
            term1_data = terms_db.get(term1)
            term2_data = terms_db.get(term2)
            
            if term1_data and term2_data:
                # Get phones with each feature
                phones1 = _get_phones_with_feature(term1)
                phones2 = _get_phones_with_feature(term2)
                
                result = f"""**{term1_data['full_name']} ({term1_data['term']}):**
{term1_data['explanation']}
Benefits: {', '.join(term1_data['benefits'])}
Use case: {term1_data['use_case']}
Phones with {term1_data['term']}: {', '.join(phones1) if phones1 else 'Check our catalog'}

**{term2_data['full_name']} ({term2_data['term']}):**
{term2_data['explanation']}
Benefits: {', '.join(term2_data['benefits'])}
Use case: {term2_data['use_case']}
Phones with {term2_data['term']}: {', '.join(phones2) if phones2 else 'Check our catalog'}"""
                return result
            else:
                # Terms not in database - out of context
                return f"I don't have information about '{term1}' or '{term2}' in my mobile phone knowledge base. I can only explain mobile phone related technical terms. Would you like to know about features like OIS, 5G, AMOLED, Fast Charging, etc.?"
    
    # Single term lookup
    term_data = terms_db.get(term_lower)
    if term_data:
        # Get phones with this feature
        phones = _get_phones_with_feature(term_data['term'])
        
        result = f"""**{term_data['full_name']} ({term_data['term']})**

{term_data['explanation']}

**Benefits:**
{chr(10).join('• ' + benefit for benefit in term_data['benefits'])}

**Use Case:** {term_data['use_case']}

**Phones in our catalog with {term_data['term']}:**
{', '.join(phones) if phones else 'Available in select models - search to find them!'}"""
        return result
    
    # Term not found - out of context question
    available_terms = sorted(set([t['term'] for t in terms_db.values() if 'term' in t]))[:10]
    return f"""I don't have information about '{term}' in my mobile phone technical terms database.

I can explain these mobile phone features: {', '.join(available_terms)}

Would you like to know about any of these? Or ask me to search for phones with specific features!"""


tools = [search_phones, compare_phones, get_phone_details, explain_technical_term]
