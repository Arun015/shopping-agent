import json
from typing import List, Optional
from pathlib import Path
from backend.dto import PhoneDTO


class PhoneDAO:
    def __init__(self, data_file: str = "backend/data/phones.json"):
        self.data_file = Path(data_file)
        self.phones: List[PhoneDTO] = []
        self._load_data()
    
    def _load_data(self):
        with open(self.data_file, 'r') as f:
            data = json.load(f)
            self.phones = [PhoneDTO(**phone) for phone in data['phones']]
    
    def get_all(self) -> List[PhoneDTO]:
        return self.phones
    
    def get_by_id(self, phone_id: int) -> Optional[PhoneDTO]:
        for phone in self.phones:
            if phone.id == phone_id:
                return phone
        return None
    
    def get_by_model(self, model: str) -> Optional[PhoneDTO]:
        model_lower = model.lower()
        for phone in self.phones:
            if model_lower in phone.model.lower() or model_lower in f"{phone.brand} {phone.model}".lower():
                return phone
        return None
    
    def search(
        self,
        budget_min: Optional[int] = None,
        budget_max: Optional[int] = None,
        brand: Optional[str] = None,
        features: Optional[List[str]] = None,
        min_camera_mp: Optional[int] = None,
        min_battery_mah: Optional[int] = None,
        min_ram_gb: Optional[int] = None
    ) -> List[PhoneDTO]:
        results = self.phones
        
        if budget_min:
            results = [p for p in results if p.price >= budget_min]
        
        if budget_max:
            results = [p for p in results if p.price <= budget_max]
        
        if brand:
            brand_lower = brand.lower()
            results = [p for p in results if p.brand.lower() == brand_lower]
        
        if features:
            features_lower = [f.lower() for f in features]
            results = [
                p for p in results 
                if any(f in [pf.lower() for pf in p.features] for f in features_lower)
            ]
        
        if min_camera_mp:
            results = [p for p in results if p.specs.camera.main_mp >= min_camera_mp]
        
        if min_battery_mah:
            results = [p for p in results if p.specs.battery_mah >= min_battery_mah]
        
        if min_ram_gb:
            results = [p for p in results if p.specs.ram_gb >= min_ram_gb]
        
        return results
    
    def sort_phones(self, phones: List[PhoneDTO], sort_by: str = "price") -> List[PhoneDTO]:
        if sort_by == "price":
            return sorted(phones, key=lambda p: p.price)
        elif sort_by == "camera":
            return sorted(phones, key=lambda p: p.specs.camera.main_mp, reverse=True)
        elif sort_by == "battery":
            return sorted(phones, key=lambda p: p.specs.battery_mah, reverse=True)
        elif sort_by == "performance":
            return sorted(phones, key=lambda p: p.specs.ram_gb, reverse=True)
        elif sort_by == "price_desc":
            return sorted(phones, key=lambda p: p.price, reverse=True)
        return phones
    
    def compare_phones(self, phone_ids: List[int]) -> List[PhoneDTO]:
        return [phone for phone in self.phones if phone.id in phone_ids]


phone_dao = PhoneDAO()



