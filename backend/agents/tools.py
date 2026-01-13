from langchain.tools import tool
from typing import List, Optional
from backend.dao import phone_dao


@tool
def search_phones(
    budget_min: Optional[int] = None,
    budget_max: Optional[int] = None,
    brand: Optional[str] = None,
    features: Optional[List[str]] = None,
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
        JSON string with matching phones
    """
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
            "camera_mp": phone.specs.camera.main_mp,
            "battery_mah": phone.specs.battery_mah,
            "processor": phone.specs.processor,
            "ram_gb": phone.specs.ram_gb,
            "storage_gb": phone.specs.storage_gb,
            "features": phone.features,
            "pros": phone.pros,
            "cons": phone.cons
        })
    
    import json
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
    
    import json
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
    
    import json
    return json.dumps(details, indent=2)


@tool
def explain_technical_term(term: str) -> str:
    """Explain technical terms related to mobile phones.
    
    Args:
        term: Technical term to explain (OIS, EIS, AMOLED, etc.)
    
    Returns:
        Explanation of the term
    """
    explanations = {
        "ois": "Optical Image Stabilization - Hardware-based camera stabilization using gyroscopes and moving lens elements. Provides better stabilization than EIS, especially in low light and for photos.",
        "eis": "Electronic Image Stabilization - Software-based stabilization that crops and shifts the image digitally. Works well for video but not available for photos.",
        "amoled": "Active Matrix Organic Light-Emitting Diode - Display technology with individual pixels that emit light. Offers deeper blacks, better contrast, and more vibrant colors than LCD.",
        "lcd": "Liquid Crystal Display - Traditional display technology that uses a backlight. Generally more affordable but can't match AMOLED's contrast and black levels.",
        "5g": "Fifth generation mobile network - Offers faster data speeds, lower latency, and better connectivity than 4G. Essential for future-proofing your device.",
        "ip67": "Ingress Protection rating 6 (dust-tight) and 7 (water resistant up to 1 meter for 30 minutes). Good protection against dust and water splashes.",
        "ip68": "Ingress Protection rating 6 (dust-tight) and 8 (water resistant beyond 1 meter). Better water resistance than IP67, typically up to 1.5 meters for 30 minutes.",
        "fast charging": "Technology that allows phones to charge at higher wattages (30W-150W) for quicker charging times. Higher wattage generally means faster charging.",
        "refresh rate": "How many times per second the display updates (measured in Hz). Higher refresh rates (90Hz, 120Hz, 144Hz) provide smoother scrolling and animations.",
        "processor": "The brain of the phone. Snapdragon and MediaTek Dimensity are common Android processors. Higher model numbers generally indicate better performance.",
        "ram": "Random Access Memory - Determines how many apps can run simultaneously. 6GB is minimum, 8GB is recommended, 12GB+ is for power users.",
        "nfc": "Near Field Communication - Enables contactless payments (Google Pay, etc.) and quick pairing with accessories.",
        "gorilla glass": "Corning's toughened glass for phone displays and backs. Higher versions (Gorilla Glass 5, Victus) offer better drop and scratch protection.",
        "telephoto": "Camera lens with optical zoom capability. Allows you to zoom in without losing quality, unlike digital zoom.",
        "ultrawide": "Camera lens with wider field of view (typically 120°). Great for landscape, group photos, and tight spaces.",
        "macro": "Close-up camera lens for photographing small objects. Usually 2-5MP and limited practical use."
    }
    
    term_lower = term.lower().strip()
    
    if term_lower in explanations:
        return explanations[term_lower]
    
    return f"Technical term '{term}' not found. Available terms: OIS, EIS, AMOLED, LCD, 5G, IP67, IP68, Fast Charging, Refresh Rate, Processor, RAM, NFC, Gorilla Glass, Telephoto, Ultrawide, Macro."


tools = [search_phones, compare_phones, get_phone_details, explain_technical_term]



