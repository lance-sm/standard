# -*- coding: utf-8 -*-
"""Vertical taxonomy + generalist/specialist rules for the Badlands broker farm.

Every pattern is a PHRASE where the bare word would be ambiguous. The point is
to record what a broker's own website claims, not what its name hints at.
"""
import re

# ---------------------------------------------------------------- verticals ---
# label -> list of regex fragments (matched case-insensitively against site text)
VERTICALS = {
    "Security & Life Safety": [
        r"security alarm", r"alarm (?:company|companies|dealer|monitoring|industry|contractor)",
        r"burglar alarm", r"fire alarm", r"life safety", r"locksmith", r"access control",
        r"video surveillance", r"\bcctv\b", r"central station", r"security integrator",
        r"security system", r"electronic security", r"physical security", r"fire protection",
        r"fire sprinkler", r"fire (?:&|and) life safety", r"security monitoring",
        r"monitored security", r"security guard", r"guard service", r"alarm installation",
        r"security (?:&|and) fire", r"systems integrator", r"low[- ]voltage",
        r"security services (?:compan|industr|sector|business)", r"perimeter security",
    ],
    "HVAC, Plumbing & Mechanical": [
        r"\bhvac\b", r"plumbing", r"mechanical contract", r"sheet metal", r"refrigeration",
        r"boiler", r"heating (?:&|and) (?:air|cooling)", r"\bhvacr\b", r"mechanical services",
    ],
    "Electrical & Low Voltage": [
        r"electrical contract", r"electrician", r"electrical services (?:compan|business|industr)",
    ],
    "Roofing & Exteriors": [r"roofing", r"\broofer", r"siding", r"gutter", r"exterior remodel"],
    "Landscaping & Lawn": [
        r"landscap(?:ing|e) (?:compan|business|industr|services|contractor|firm|maintenance|design)",
        r"lawn care", r"tree (?:service|care)", r"irrigation", r"snow removal",
    ],
    "Pest Control": [r"pest control", r"exterminat", r"termite"],
    "Construction & Building Products": [
        r"construction (?:compan|industr|business|firm|sector|services)", r"general contract",
        r"building product", r"concrete", r"masonry", r"excavat", r"paving", r"civil construction",
    ],
    "Healthcare Practices": [
        r"healthcare (?:practice|business|compan|industr|services|sector)", r"medical practice",
        r"physician practice", r"medical group", r"behavioral health", r"dermatolog",
        r"ophthalmolog", r"optometr", r"orthopedic", r"urgent care", r"\bmed spa\b",
        r"medical device", r"health system", r"radiolog", r"anesthesiolog", r"physical therapy",
    ],
    "Dental": [r"dental", r"dentist", r"orthodont", r"endodont", r"periodont", r"\bdso\b"],
    "Veterinary": [r"veterinar", r"\bvet (?:practice|clinic|hospital)", r"animal hospital"],
    "Senior Care & Home Health": [
        r"senior (?:care|living|housing)", r"assisted living", r"home care", r"home health",
        r"hospice", r"skilled nursing", r"long[- ]term care",
    ],
    "Pharmacy": [r"pharmac(?:y|ies)", r"compounding pharmac"],
    "Accounting & Tax": [
        r"\bcpa\b", r"accounting (?:practice|firm|business|compan)", r"tax (?:practice|firm)",
        r"bookkeeping", r"audit firm",
    ],
    "Insurance Agencies": [
        r"insurance agenc", r"insurance broker", r"insurance book of business",
        r"benefits agenc", r"\bmga\b", r"third[- ]party administrator",
    ],
    "Wealth Management & Financial Services": [
        r"wealth management", r"registered investment advis", r"\bria\b", r"financial advisory practice",
        r"financial planning practice", r"mortgage (?:compan|broker|bank)", r"specialty finance",
        r"asset management (?:firm|business)", r"fintech",
    ],
    "Legal": [r"law (?:firm|practice)", r"legal (?:practice|services (?:firm|business))", r"title agenc"],
    "IT, MSP & Software": [
        r"managed service provider", r"\bmsp\b", r"managed it", r"it service provider", r"information technology (?:compan|services|business)",
        r"\bsaas\b", r"software (?:compan|business|develop|product)", r"cybersecurity",
        r"cloud (?:services|hosting|provider)", r"\bmssp\b", r"data cent(?:er|re)", r"technology services",
    ],
    "Staffing & HR": [
        r"staffing", r"recruit(?:ing|ment) (?:firm|agenc|business)", r"\bpeo\b",
        r"human resources outsourc", r"executive search",
    ],
    "Marketing & Creative Agencies": [
        r"marketing agenc", r"advertising agenc", r"digital agenc", r"creative agenc",
        r"\bseo\b", r"public relations (?:firm|agenc)", r"media buying",
    ],
    "Manufacturing & Industrial": [
        r"manufactur", r"machin(?:ing|e shop)", r"fabricat", r"industrial (?:compan|business|services|sector)",
        r"\bcnc\b", r"metal (?:form|stamp|work)", r"tool (?:&|and) die", r"foundr", r"job shop",
        r"precision machin", r"contract manufactur",
    ],
    "Packaging": [r"packaging", r"corrugat", r"label (?:printing|converter)", r"flexible packaging"],
    "Chemicals & Plastics": [r"chemical (?:compan|business|manufactur|industr)", r"plastics", r"injection molding", r"specialty chemical", r"coatings"],
    "Aerospace, Defense & GovCon": [
        r"aerospace", r"\bdefen[cs]e (?:contract|industr|compan|sector)", r"government contract",
        r"\bgovcon\b", r"\bdod\b", r"federal (?:contract|services)",
    ],
    "Automotive": [
        r"automotive", r"auto (?:repair|body|dealer|part)", r"collision (?:repair|cent)",
        r"car (?:dealer|wash)", r"tire (?:shop|dealer|business)", r"powersports",
    ],
    "Transportation & Logistics": [
        r"trucking", r"logistics", r"freight", r"transportation (?:compan|business|industr|services)",
        r"\b3pl\b", r"last[- ]mile", r"fleet (?:services|maintenance)", r"moving (?:&|and) storage",
    ],
    "Food, Beverage & Restaurants": [
        r"restaurant", r"food (?:&|and) beverage", r"food manufactur", r"food service",
        r"bakery", r"brewer", r"distiller", r"winer", r"catering", r"\bqsr\b", r"food distribut",
    ],
    "Retail, E-commerce & Consumer": [
        r"\be-?commerce\b", r"retail (?:compan|business|chain|industr|store)", r"consumer product",
        r"\bcpg\b", r"amazon (?:seller|\bfba\b)", r"direct[- ]to[- ]consumer", r"\bdtc\b",
    ],
    "Hospitality & Travel": [
        r"hospitality", r"hotel", r"resort", r"travel (?:agenc|business|compan)", r"restaurant (?:&|and) hospitality",
    ],
    "Real Estate & Property": [
        r"real estate", r"property management", r"self[- ]storage", r"commercial real estate",
        r"\bcre\b", r"\bhoa\b management", r"apartment",
    ],
    "Education & Childcare": [
        r"child ?care", r"day ?care", r"early childhood", r"education (?:compan|business|sector|services)",
        r"tutoring", r"charter school", r"\bedtech\b", r"private school", r"training (?:compan|business)",
    ],
    "Cannabis": [r"cannabis", r"dispensar", r"\bhemp\b", r"\bcbd\b"],
    "Energy, Environmental & Utilities": [
        r"\bsolar\b", r"renewable energy", r"oil (?:&|and) gas", r"\boilfield\b", r"environmental services",
        r"waste (?:management|hauling|services)", r"water treatment", r"utility (?:services|contract)",
        r"energy (?:services|efficiency|industr|sector)", r"propane",
    ],
    "Funeral & Cemetery": [r"funeral", r"cemeter", r"cremation", r"deathcare"],
    "Fitness, Salon & Wellness": [
        r"\bgym\b", r"fitness", r"salon", r"day spa", r"\bmed(?:ical)? spa\b", r"wellness (?:business|compan|cent)",
        r"barbershop", r"tattoo",
    ],
    "Agriculture": [r"agricultur", r"agribusiness", r"farming (?:operation|business)", r"row crop", r"crop production", r"dairy"],
    "Printing & Signage": [r"printing (?:compan|business|industr)", r"\bsignage\b", r"sign (?:compan|shop)", r"commercial print", r"wide[- ]format"],
    "Cleaning & Facilities Services": [
        r"janitorial", r"commercial cleaning", r"facilit(?:y|ies) (?:services|management|maintenance)",
        r"restoration (?:compan|business|services)", r"laundr", r"\bpressure washing\b",
    ],
    "Engineering & Architecture": [
        r"engineering (?:firm|compan|services|business)", r"architect(?:ure|ural) (?:firm|practice|services|design)", r"architects? (?:&|and) engineers", r"\ba\/e\b",
        r"surveying", r"\bmep\b", r"geotechnical", r"environmental consult",
    ],
    "Media & Entertainment": [r"media (?:compan|business)", r"publishing", r"broadcast", r"entertainment (?:compan|industr)", r"film (?:&|and) television", r"gaming"],
    "Telecom": [r"telecom", r"wireless (?:infrastructure|carrier)", r"fiber (?:optic|network)", r"\bisp\b", r"cell tower"],
    "Pharma & Life Sciences": [r"pharmaceutic", r"life science", r"biotech", r"clinical (?:research|trial)", r"\bcdmo\b"],
    "Distribution & Wholesale": [r"distribut(?:ion|or) (?:compan|business|industr)", r"wholesale", r"industrial distribut", r"value[- ]added reseller"],
    "Nonprofit & Associations": [r"nonprofit", r"not[- ]for[- ]profit", r"association management"],
}

# Verticals we never treat as a "specialisation" on their own when they are the
# only hit, because almost every M&A site mentions them in boilerplate.
WEAK_ALONE = {"Real Estate & Property", "Wealth Management & Financial Services", "Legal"}
WEAK_ALONE_MIN = 6

# ------------------------------------------------------------- generalist ----
GENERALIST_PHRASES = [
    r"all industr", r"any industr", r"every industr", r"across (?:all )?industr",
    r"industry[- ]agnostic", r"all sectors", r"any sector", r"variety of industr",
    r"wide (?:range|variety) of industr", r"range of industr", r"diverse (?:set of )?industr",
    r"many industr", r"multiple industr", r"all types of business", r"any type of business",
    r"all kinds of business", r"regardless of industry", r"no industry (?:focus|preference)",
    r"generalist", r"main street business", r"businesses of all", r"industries we serve include",
    r"broad range of (?:industr|sector|business)", r"most industr",
]

SPECIALIST_PHRASES = [
    r"we (?:only|exclusively) (?:work|represent|serve|advise|sell)", r"exclusively (?:focus|serve|represent|dedicated)",
    r"sole(?:ly)? focus", r"niche (?:focus|practice|expertise)", r"specializ\w* (?:exclusively|solely)",
    r"the only (?:broker|advisor|firm|investment bank)", r"dedicated (?:exclusively|solely)",
    r"industry[- ]focused", r"sector specialist", r"only (?:broker|advisor|firm) (?:that|who)",
]

# ------------------------------------------------- security-deal evidence ----
# Security-industry words that count when found near transaction language.
# HARD: language that only ever means physical security / life safety.
PHYSICAL_HARD = [
    r"(?<!false )\balarms?\b", r"burglar", r"fire alarm", r"life safety", r"locksmith",
    r"video surveillance", r"\bcctv\b", r"central station", r"fire protection",
    r"fire sprinkler", r"security guard", r"guard service", r"door hardware",
    r"\brmr\b", r"recurring monthly revenue", r"perimeter security", r"monitored security",
    r"fire (?:&|and) life safety", r"fire suppression",
]
# STRONG: physical in almost every context, but can overlap cyber wording.
PHYSICAL_STRONG = PHYSICAL_HARD + [
    r"access control", r"security system", r"electronic security", r"physical security",
    r"security monitoring", r"security (?:&|and) fire", r"fire (?:&|and) security",
    r"security integrator",
]
# AMBIGUOUS: could be a cyber firm just as easily - never enough on its own.
PHYSICAL_WEAK = [
    r"security compan", r"security services", r"systems integrator", r"low[- ]voltage",
    r"security business", r"security industry",
]
# Cyber wording. If present, only HARD language still counts as physical security.
CYBER_TERMS = [
    r"cyber", r"infosec", r"information security", r"network security", r"data security",
    r"endpoint", r"\bsoc 2\b", r"penetration test", r"managed security service",
    r"application security", r"cloud security", r"identity (?:&|and) access management",
    r"\bsiem\b", r"threat (?:intel|detect)", r"\bmssp\b", r"secure network",
    r"\bit security\b", r"software", r"\bsaas\b",
]

SECURITY_DEAL_TERMS = [
    r"security alarm", r"alarm (?:compan|dealer|monitoring|business|account)", r"burglar alarm",
    r"fire alarm", r"life safety", r"locksmith", r"access control", r"video surveillance",
    r"\bcctv\b", r"central station", r"security integrator", r"security system",
    r"electronic security", r"physical security", r"fire protection", r"fire sprinkler",
    r"security monitoring", r"monitored security", r"security guard", r"guard service",
    r"systems integrator", r"security (?:&|and) fire", r"fire (?:&|and) security",
    r"security services", r"security compan", r"\brmr\b", r"recurring monthly revenue",
]

TRANSACTION_TERMS = [
    r"has been acquired", r"\bacquired by\b", r"\bacquisition of\b", r"\bsale of\b", r"\bsold to\b",
    r"has (?:been )?sold", r"merger", r"recapitaliz", r"divest", r"\bdivestiture\b",
    r"advised", r"represented", r"served as (?:exclusive )?(?:financial )?advisor",
    r"completed (?:the )?(?:sale|transaction|acquisition)", r"closed (?:the )?(?:sale|transaction)",
    r"successfully sold", r"exclusive (?:sell|buy)[- ]side", r"\bwas acquired\b",
    r"\bhas acquired\b", r"\bpurchased by\b", r"\bexit\b", r"\bclient success\b",
]
# Page furniture: proves a deal PAGE, not a deal sentence.
TRANSACTION_WEAK = [r"transaction", r"tombstone", r"\bdeals?\b", r"case stud", r"track record"]

# URL/title hints that a page is a transaction list
DEAL_PAGE_HINTS = [
    "transaction", "deal", "tombstone", "closed", "completed", "case-stud", "casestud",
    "experience", "portfolio", "success", "our-work", "ourwork", "represent", "sold",
    "engagement", "track-record", "trackrecord", "recent",
]
VERTICAL_PAGE_HINTS = [
    "industr", "sector", "specialt", "specializ", "practice-area", "practicearea",
    "expertise", "market", "who-we-serve", "whoweserve", "vertical", "niche", "focus",
    "what-we-do", "whatwedo", "services",
]

def _compile(frags):
    return re.compile("|".join("(?:%s)" % f for f in frags), re.I)

VERTICAL_RE = {k: _compile(v) for k, v in VERTICALS.items()}
GENERALIST_RE = _compile(GENERALIST_PHRASES)
SPECIALIST_RE = _compile(SPECIALIST_PHRASES)
SECURITY_RE = _compile(SECURITY_DEAL_TERMS)
PHYSICAL_HARD_RE = _compile(PHYSICAL_HARD)
PHYSICAL_STRONG_RE = _compile(PHYSICAL_STRONG)
PHYSICAL_WEAK_RE = _compile(PHYSICAL_WEAK)
CYBER_RE = _compile(CYBER_TERMS)
TRANSACTION_RE = _compile(TRANSACTION_TERMS)
TRANSACTION_WEAK_RE = _compile(TRANSACTION_WEAK)
ALL_KEYWORD_RE = _compile(
    [f for v in VERTICALS.values() for f in v]
    + GENERALIST_PHRASES + SPECIALIST_PHRASES + SECURITY_DEAL_TERMS
    + PHYSICAL_HARD + PHYSICAL_STRONG + PHYSICAL_WEAK
    + TRANSACTION_TERMS + TRANSACTION_WEAK
)
