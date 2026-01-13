import re
from typing import Tuple


class SafetyService:
    
    ADVERSARIAL_PATTERNS = [
        r"ignore\s+(previous|above|all|your)\s+(instructions?|rules?|prompts?)",
        r"reveal\s+(your\s+)?(system\s+)?(prompt|instructions?|rules?)",
        r"what\s+(is|are)\s+your\s+(instructions?|rules?|prompts?)",
        r"show\s+(me\s+)?(your\s+)?(system\s+)?(prompt|instructions?)",
        r"(api|secret|private)\s*key",
        r"bypass\s+(security|safety|rules?)",
        r"pretend\s+(you|to)\s+(are|be)",
        r"act\s+as\s+(if|a|an)",
        r"roleplay",
        r"jailbreak",
        r"dan\s+mode",
        r"developer\s+mode",
    ]
    
    TOXIC_PATTERNS = [
        r"\b(trash|garbage|shit|crap|sucks?)\s+(brand|phone|company)",
        r"(brand|phone|company)\s+(is|are)\s+(trash|garbage|shit|crap|sucks?)",
        r"(hate|worst|terrible|awful)\s+(brand|phone)",
    ]
    
    OFF_TOPIC_KEYWORDS = [
        "weather", "news", "politics", "recipe", "cooking", "movie", "song",
        "game", "sport", "football", "cricket", "stock", "investment",
        "health", "medical", "doctor", "medicine", "disease"
    ]
    
    @staticmethod
    def is_adversarial(message: str) -> Tuple[bool, str]:
        message_lower = message.lower()
        
        for pattern in SafetyService.ADVERSARIAL_PATTERNS:
            if re.search(pattern, message_lower):
                return True, "I'm here to help you find the perfect mobile phone. I can't assist with that request."
        
        return False, ""
    
    @staticmethod
    def is_toxic(message: str) -> Tuple[bool, str]:
        message_lower = message.lower()
        
        for pattern in SafetyService.TOXIC_PATTERNS:
            if re.search(pattern, message_lower):
                return True, "I maintain a neutral and factual approach. I can provide objective comparisons if you'd like."
        
        return False, ""
    
    @staticmethod
    def is_off_topic(message: str) -> Tuple[bool, str]:
        message_lower = message.lower()
        
        if len(message_lower.split()) < 3:
            return False, ""
        
        phone_keywords = ["phone", "mobile", "smartphone", "camera", "battery", "processor", "ram", "display"]
        has_phone_context = any(keyword in message_lower for keyword in phone_keywords)
        
        if has_phone_context:
            return False, ""
        
        off_topic_count = sum(1 for keyword in SafetyService.OFF_TOPIC_KEYWORDS if keyword in message_lower)
        
        if off_topic_count >= 1:
            return True, "I specialize in helping with mobile phone shopping. How can I assist you in finding the right phone?"
        
        return False, ""
    
    @staticmethod
    def validate_input(message: str) -> Tuple[bool, str]:
        if not message or len(message.strip()) == 0:
            return False, "Please provide a message."
        
        if len(message) > 500:
            return False, "Message too long. Please keep it under 500 characters."
        
        is_adv, adv_msg = SafetyService.is_adversarial(message)
        if is_adv:
            return False, adv_msg
        
        is_tox, tox_msg = SafetyService.is_toxic(message)
        if is_tox:
            return False, tox_msg
        
        is_off, off_msg = SafetyService.is_off_topic(message)
        if is_off:
            return False, off_msg
        
        return True, ""


safety_service = SafetyService()
