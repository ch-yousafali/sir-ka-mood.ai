import os
import json
import random
import unicodedata
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

DISCLAIMER = "Disclaimer: Ye sab ek comedy platform hai. Kisi professor, department ya university ke against koi personal baat nahi hai. Sab moh maya hai. Marks toh ek number hain — trauma asli hai."

# ─────────────────────────────────────────────
# Punjab University Official Contact Integration
# ─────────────────────────────────────────────
PU_CONTACTS = {
    "vc": {
        "name": "Prof. Dr. Muhammad Ali",
        "title": "Vice Chancellor, University of the Punjab",
        "email": "vc@pu.edu.pk",
        "address": "Vice Chancellor's Office, University of the Punjab, Lahore"
    },
    "controller": {
        "name": "Controller of Examinations",
        "title": "Controller of Examinations, University of the Punjab",
        "email": "controller@pu.edu.pk",
        "address": "Examination Branch, University of the Punjab, Lahore"
    },
    "chep": {
        "name": "Chairman, CHEP",
        "title": "Chairman, Centre for High Energy Physics, University of the Punjab",
        "email": "chep@pu.edu.pk",
        "address": "CHEP, University of the Punjab, Quaid-e-Azam Campus, Lahore"
    },
    "it": {
        "name": "Director IT",
        "title": "Director, IT Services, University of the Punjab",
        "email": "itservices@pu.edu.pk",
        "address": "IT Department, University of the Punjab, Lahore"
    }
}

# ─────────────────────────────────────────────
# Load student database — properly resolved
# ─────────────────────────────────────────────
_base = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(_base, 'students.json'), encoding='utf-8') as f:
    _db = json.load(f)

ALL_STUDENTS = _db['evening'] + _db['morning']


def normalize(s):
    s = s.strip().upper()
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return s


def find_student(roll_no=None, name=None):
    roll_no = normalize(roll_no) if roll_no else ''
    name    = normalize(name)    if name    else ''

    if roll_no:
        for s in ALL_STUDENTS:
            if normalize(s['roll_no']) == roll_no:
                return s

    if name:
        input_words = set(name.split())
        for s in ALL_STUDENTS:
            db_words = set(normalize(s['name']).split())
            if input_words & db_words:
                return s

    return None


# ─────────────────────────────────────────────────────────────────
#  50 THEORY TYPES  — expanded across life domains
#  Categories: dreams, astronomy, food, domestic, cricket, economy,
#              WhatsApp, tech failures, philosophy, mythology, etc.
# ─────────────────────────────────────────────────────────────────
THEORY_TYPES = {

    # ── DISASTER ZONE (0–4) ──
    (0, 4): {
        "name": "Paper Dekh Ke Coma",
        "vibe": "Sir saw your paper and needed medical attention",
        "variations": [
            "Sir ne aapka paper uthaya, ek line padha, aur seedha hospital call kia — chest pain ho gayi unhe on the spot",
            "Sir ne aapki answer sheet scan ki, printer ne bhi print karne se saaf mana kar diya — sharam ki wajah se",
            "Sir ne aapki copy ko 'Exhibit A — Evidence ke khilaf education system' label kaar ke department mein frame karwa diya"
        ]
    },

    # ── SUPERNOVA DISASTER (5–9) ──
    (5, 9): {
        "name": "Cosmic Punishment",
        "vibe": "Stars aligned against you specifically",
        "variations": [
            "NASA ne confirm kia hai ke Mars retrograde tha usi raat jo Sir ne paper check kia — ye galactic influence hai",
            "Sir ne raat ko taaron ki taraf dekha tha, ek tara toot ke gira — unho ne socha 'is student ki qismat gayi', aur marks usi omen ka nateeja hain",
            "Jupiter ki gravity ne Sir ke pen ko slow kar diya tha, isliye marks mein numbers khatam ho gaye"
        ]
    },

    # ── NIGHTMARE MARKING (10–14) ──
    (10, 14): {
        "name": "Neend Mein Khwab Bura Aaya",
        "vibe": "Sir was checking papers in a nightmare",
        "variations": [
            "Sir raat 3 baje sapne mein paper check kar rahe thay, sapne mein aapka page aaya, unhone neend mein hi marks daal diye — subah wahi copy real nikli",
            "Sir ko sapne mein ek bhoot mila jisne kaha 'is student ko zyada mat dena' — Sir darr gaye, orders follow kiye",
            "Sir ne REM sleep mein aapki copy imaginary pen se check ki, aur woh imaginary marks somehow transfer ho gaye real sheet pe"
        ]
    },

    # ── BIWI KA BADLA Level 1 (15–19) ──
    (15, 19): {
        "name": "Biwi Ka Badla — Level 1",
        "vibe": "Domestic chaos leaked directly into marking",
        "variations": [
            "Biwi ne subah jootay maare thay Sir ko — unhone ghusa seedha aapke marks pe nikaala, safe target mila",
            "Biwi ne keh diya 'tum kuch nahi kar sakte' — Sir ne prove kia aapke number kaat ke, indirect revenge",
            "Ghar pe puri raat larai thi, Sir office aaye, aapki copy sabse pehle mili — wrong place, wrong time, wrong century"
        ]
    },

    # ── BIWI KA BADLA Level 2 (20–24) ──
    (20, 24): {
        "name": "Biwi Ka Badla — Level 2",
        "vibe": "Sir was emotionally shattered before marking",
        "variations": [
            "Biwi ne Sir ka phone check kia tha raat ko — 23 WhatsApp messages ek unknown number se thay — subah ka mood puri class ne bhara",
            "Sasural wale aa rahe thay, tension mein Sir ke haath kaanpte thay — marks usi tremor ka nateeja hain",
            "Biwi ne keh diya 'mere abba se kum ho tum' — Sir ne ego ka hisaab aapki copy pe nikaala, baap ka nahi le sakte, tumhara le liya"
        ]
    },

    # ── PETROL CRISIS (25–29) ──
    (25, 29): {
        "name": "Petrol 300+ Wala Sadma",
        "vibe": "Economic depression hit Sir personally",
        "variations": [
            "Petrol rate 300 se upar gaya tha usi hafte — Sir depressed ho gaye, dil se kisi ko pass karna afford nahi kar rahe thay",
            "Sir ne CNG ki line mein 3 ghante waste kiye, ghusa aapke marks mein nikaala — aap gaye CNG wali queue ke saath",
            "Sir ne EMI + petrol + grocery + school fees calculate kiya ek hi din — calculator ne error dia, marks bhi usi confusion mein gaye"
        ]
    },

    # ── ASTRONOMY THEORY (30–34) ──
    (30, 34): {
        "name": "Solar Flare Ka Asar",
        "vibe": "Sun had a bad day and your marks paid for it",
        "variations": [
            "NASA ne X-class solar flare report ki thi — electromagnetic radiation ne Sir ke brain mein marking algorithm ko temporarily corrupt kar diya",
            "Solar flare ki wajah se Sir ke pen ki ink ek particular angle pe giri, jo coincidentally fail marks bani — physics ne betray kia",
            "Sir ki smartwatch ne solar activity alert diya tha — distraction mein kuch zyada numbers kaat gaye, notice nahi kia"
        ]
    },

    # ── CRICKET MATCH CURSE (35–39) ──
    (35, 39): {
        "name": "Cricket Match Ka Qarz",
        "vibe": "Pakistan lost and you personally paid",
        "variations": [
            "Pakistan ne match haar liya tha — Sir ne national dard mein seedha aapke paper pe ghusa nikaala, innocent student ka qaatil match schedule tha",
            "Sir ne match pe bet lagayi thi 5000 ki, haar gaye — aapke marks usi financial loss ka emotional chalan hain",
            "Sir ka favorite player golden duck pe out hua tha — Sir ne socha 'aaj sabko out karunga', aap pehle aaye"
        ]
    },

    # ── TECHNOLOGY FAILURE THEORY (40–44) ──
    (40, 44): {
        "name": "Technology Ne Betray Kia",
        "vibe": "Sir's tech malfunction caused your mark malfunction",
        "variations": [
            "Sir ke laptop ne paper khulte waqt BSOD dia — restart ke baad jo marks daale woh trauma mein diye, count nahi kiye properly",
            "Sir ke phone ki battery 1% pe aa gayi thi results portal fill karte waqt — kuch numbers type hi nahi hue, jo tha woh save ho gaya",
            "Sir ne Excel mein marks daale thay, AutoFill ne galat formula apply kia — Sir ne notice kia, lekin tab tak save ho chuka tha 'officially'"
        ]
    },

    # ── CHAI TRAUMA (45–49) ──
    (45, 49): {
        "name": "Chai Mein Cheeni Na Thi",
        "vibe": "Sir's morning ritual was violently destroyed",
        "variations": [
            "Chai mein cheeni bilkul zero thi — Sir ka pura din kharab hua, marking mein wo bitterness dikhti hai clearly",
            "Chai wala bhai chutti pe tha, substitute ne bland chai di — Sir ne socha 'bland day, bland marks'",
            "Chai thandi the jab Sir ne pi — cold chai, cold heart, cold marks. Simple equation."
        ]
    },

    # ── CANTEEN TRAGEDY (50–54) ──
    (50, 54): {
        "name": "Canteen Band Tha",
        "vibe": "Hunger-driven marking decisions",
        "variations": [
            "Canteen band thi, Sir bhooke pet checking karte rahe — mercy marks bhi mercy nahi lage jab bhook lagi ho",
            "Sir ne subah se kuch nahi khaya tha — hangry state mein kisi ki taraf bhi nahi socha, marks mechanically diye",
            "Sir ne diet plan start kia tha usi din — dono cheezein adhoori rahi: diet bhi, marks bhi"
        ]
    },

    # ── SLEEP DEPRIVATION (55–59) ──
    (55, 59): {
        "name": "Neend Poori Nahi Hui",
        "vibe": "Sir barely survived morning checking",
        "variations": [
            "Sir raat 2 baje soye, subah 6 baje uth ke paper check kia — ye marks neend ki kami ka byproduct hain, aap ka copy koi cushion nahi tha",
            "Sir ne 10 minute ka nap lia tha checking ke beech, 2 ghante nikal gaye — jaldi mein jo numbers sujhe daal diye",
            "Sir ke bachay ne raat bhar roya — subah ki marking emotionally defeated insaan ne ki, aap lucky ho itna mila"
        ]
    },

    # ── WHATSAPP FAMILY GROUP (60–64) ──
    (60, 64): {
        "name": "Family Group Ka Hazaar",
        "vibe": "Family WhatsApp group drama during marking",
        "variations": [
            "Family WhatsApp group pe 67 unread messages thay — Sir ne checking ke beech reply kia, jo marks likhte waqt pichle message ka number yaad tha woh likh diya",
            "Sir ne forwarded message padha 'marks toh sirf numbers hain' — usi ne inspire kia ye dene ko, philosophical moment",
            "Biwi ka 9-minute voice note aaya tha — Sir ne suna, marks dene mein double jaldi ki, calculator chhod ke mental math ki"
        ]
    },

    # ── BIRYANI RACE (65–69) ──
    (65, 69): {
        "name": "Biryani Se Race",
        "vibe": "Sir was racing against the canteen closing",
        "variations": [
            "Canteen mein special biryani sirf 12:30 tak thi — Sir ne jaldi mein neutral-ish marks diye aur bhaag gaye, aap usi rush ka shikaar hain",
            "Sir ne daal chawal khaya tha, satisfaction mein autopilot marking ki — na zyada socha, na kam",
            "Sir ne socha 'bas ye batch khatam karo phir khana' — aap woh 'bas khatam karo' batch hain, marks usi urgency mein nikalay"
        ]
    },

    # ── MYTHOLOGY THEORY (70–74) ──
    (70, 74): {
        "name": "Qismat Ka Likha",
        "vibe": "Written in destiny, verified by Sir",
        "variations": [
            "Aapke marks janm se hi likh diye gaye thay — Sir sirf qalam-bardaar thay, fate ne dictate kia",
            "Taqdeer mein ye hi tha — Sir ne socha bahut, lekin ek ghaib awaaz ne haath rok diya jab zyada marks likhne lage thay",
            "Ye marks cosmic plan ka hissa hain — universe chaahta hai aap mehnat karo, shortcut se aage na niklo"
        ]
    },

    # ── CRICKET JIT GAYA (75–79) ──
    (75, 79): {
        "name": "Pakistan Jeet Gaya",
        "vibe": "National euphoria = unexpectedly better marks",
        "variations": [
            "Pakistan ne match jeet lia tha — Sir ne national josh mein achi marks di, aap beneficiary bane ek historic victory ke",
            "Sir ne match pe 500 rupay jeetey thay — usi khushi mein generous ho gaye, aap lucky draw winner ho basically",
            "Sir ka favorite batsman century maar gaya tha — wo adrenaline marking mein convert hua, aap right time pe the"
        ]
    },

    # ── SUNDAY MOOD (80–84) ──
    (80, 84): {
        "name": "Sir Ko Laga Sunday Hai",
        "vibe": "Sir forgot it was a weekday",
        "variations": [
            "Sir ne accidentally socha tha aaj Sunday hai — relaxed holiday mood mein befikar marking ki, marks ka fayda aapko hua",
            "Sir ne Friday anticipation mein checking ki — weekend ki khushi advance mein release hui aapke paper pe",
            "Sir ne socha 'bas 2 din aur, phir chutti' — usi cheer mein achi marks diye bina zyada soche"
        ]
    },

    # ── CHAI PILAYI THI (85–89) ──
    (85, 89): {
        "name": "Chai Pilayi Thi",
        "vibe": "You successfully bribed Sir with tea",
        "variations": [
            "Aap ne Sir ko special elaichi chai pilayi thi semester mein — marks usi long-term investment ka compound ROI hain",
            "Chai mein extra cheeni aur love thi — Sir ne sweetness points marks mein convert kiye, unofficial exchange rate active tha",
            "Thand mein garam chai di thi aap ne Sir ko — dil pighla, marks mein convert hua, official bribe record ho gaya"
        ]
    },

    # ── FAVORITE STUDENT (90–94) ──
    (90, 94): {
        "name": "Laadla Student Theory",
        "vibe": "Teacher's pet status fully confirmed",
        "variations": [
            "Sir ne aapko apne bete jaisa samajh lia hai officially — beta ko itne hi marks milte hain, legacy maintained",
            "Aap ne Sir ki car wash ki thi last month — ye marks usi unauthorized service contract ka formal payment hain",
            "Sir ne aapki assignment apni research paper mein cite kia tha — ye co-authorship royalty marks hain, legally binding"
        ]
    },

    # ── SIR NE KHUD SOLVE KIA (95–100) ──
    (95, 100): {
        "name": "Sir Ne Khud Likha Aapka Paper",
        "vibe": "Sir literally improved your paper himself",
        "variations": [
            "Sir ne aapke paper pe khud answers likhe thay checking ke waqt — aap exam mein so rahe thay, Sir ne socha 'iska future main hoon'",
            "Sir ne socha 'ye mera intellectual heir hai' aur red pen se green answers add kiye — ye marks Sir ki mehnat hain, credit unko do",
            "Sir ne aapke wrong answers ko correct answers se replace kar diya tha silently — 'koi nahi dekhega' unho ne socha, aur sahi socha"
        ]
    },
}


# ─── BONUS THEORIES — more life domains ───────────────────────────────────────
BONUS_THEORIES = [

    # Blank paper
    {
        "range": (0, 0),
        "name": "Kagaz Pe Naam Bhi Nahi",
        "vibe": "Sir questioned if you even exist",
        "variations": [
            "Sir ne aapki copy uthaya, sirf roll number tha — 3 ghante baad bhi yahi socha ja raha hai 'ye student real hai?'",
            "Aap ne paper mein apna naam likh ke free-hand art ki — zero art score hai unfortunately",
            "Sir ne socha 'shayad invisible ink hai' — UV light, roshni, magnifying glass — kuch nahi mila, zero confirmed"
        ]
    },

    # Dream theory — special range
    {
        "range": (11, 13),
        "name": "Sir Ka Sapna — Very Bad Wala",
        "vibe": "Sir literally checked papers in a nightmare",
        "variations": [
            "Sir raat ko ek bhayanak sapna dekh rahe thay jisme aapka paper tha — neend mein socha 'ye student mujhe tang karega' — marks usi dream logic pe decide hue",
            "Sir ko sapne mein ek giant red pen mila jo automatically wrong likhhta tha — aap usi automatic mode ke shikaar hain",
            "Freud ne kaha tha ke sapne subconscious reveal karte hain — Sir ka sapna reveal karta hai ke aapke marks unhe personally disturb karte hain"
        ]
    },

    # Inflation theory
    {
        "range": (26, 29),
        "name": "Inflation Ka Direct Hit",
        "vibe": "Sir counted marks like counting rupees",
        "variations": [
            "Sir ne market se 1 kg chicken ka rate suna — shock mein aur marks nahi diye, saving mode activate tha",
            "Bijli ka bill 45,000 aaya tha — marks utne hi kaat ke 'balance' restore kiya, household accounting is marks se linked hai",
            "Sir ne dollar-rupee rate dekha tha usi din — marks bhi usi devaluation mein convert ho gaye automatically"
        ]
    },

    # Attendance theory
    {
        "range": (18, 22),
        "name": "Attendance Wala Pass",
        "vibe": "Sir gave marks purely for showing up alive",
        "variations": [
            "Sir ne socha 'kam se kam aata toh hai' — attendance loyalty marks hain ye, academics optional samjha",
            "Aap ne har class mein 'present sir' bol diya — ye marks usi verbal effort ka recognition hain",
            "Sir ne roll call mein aapka naam sun ke 'acha' keh diya tha ek baar — usi moment ka delayed cash back ye marks hain"
        ]
    },

    # Philosophy theory
    {
        "range": (47, 53),
        "name": "Existential Crisis Ke Marks",
        "vibe": "Sir had a philosophical breakdown while marking",
        "variations": [
            "Sir ne checking ke waqt socha 'marks ka matlab kya hai, zindagi ka matlab kya hai' — 15 minute mein existential crisis, aapke marks usi episode ka output hain",
            "Sir ne Nietzsche padha tha usi hafte — 'God is dead' wale vibe mein marks bhi kill kiye gaye",
            "Sir ke haath kaanp rahe thay 50 likhte waqt — ye marks 'pass karoon ya fail' ke existential debate ka ceasefire nateeja hain"
        ]
    },

    # Technology failure 2
    {
        "range": (38, 43),
        "name": "Sir Ka Phone Dead Tha",
        "vibe": "Dead battery = dead marking accuracy",
        "variations": [
            "Sir ke phone ki battery 2% thi results portal fill karte waqt — keyboard lag mein jo numbers type hue woh save ho gaye, verify karna possible nahi tha",
            "Sir ka internet 3G pe aa gaya tha portal pe — loading ke beech jo numbers dikh rahe thay woh cached version thay, galat data submit hua",
            "Sir ne wrong tab mein marks daale thay — tab close karte waqt 'Save' click hua, 'Discard' nahi — ye marks technical negligence hain"
        ]
    },

    # Average ka badshah
    {
        "range": (58, 63),
        "name": "Mediocrity Ka Certificate",
        "vibe": "Perfectly, painfully, precisely average",
        "variations": [
            "Sir ne aapka paper dekh ke kaha 'bilkul beech ka student' — ye mediocrity certificate hai, frameable option available hai",
            "Aap ne na kuch outstanding kia, na kuch catastrophic — Sir ne awarded average marks to average paper, brutal fairness",
            "Sir ne aapki copy dekhi, chai pi, wapas dekhi — marks nahi badle, chai bhi khatam ho gayi"
        ]
    },

    # Almost topper
    {
        "range": (77, 83),
        "name": "Distinction Se Ek Kadam Door",
        "vibe": "Painfully close to glory",
        "variations": [
            "Aap distinction ke itne paas thay ke Sir ne dard se marks kaate — 'humility seekho' tha Sir ka unofficial message",
            "Sir ne socha '80+ de deta hoon toh sir pe charh jaega' — strategic marks diye, ego management 101",
            "Aap ne Sir ko impress kia tha, lekin Sir ne dikhaya nahi publicly — ye chhupa hua appreciation ke marks hain, awkward version"
        ]
    },

    # Dream theory — high marks
    {
        "range": (88, 93),
        "name": "Sir Ka Sapna — Acha Wala",
        "vibe": "Sir had a wonderful dream and you benefited",
        "variations": [
            "Sir ko sapne mein aapka future dikh gaya — ek successful physicist — unhone socha 'is potential ko marks se nahi rokna' — boom, ye marks",
            "Sir ke sapne mein aap ne unhe Nobel Prize acceptance speech mein thank kia — woh itne khush hue ke real life mein marks badh gaye",
            "Sir ne neend mein aapki copy check ki aur subconscious ne bola 'ye student theek hai yaar' — marks usi positive subconscious review hain"
        ]
    },

    # Mythology / fate high marks
    {
        "range": (93, 96),
        "name": "Sifarish Ki Theory",
        "vibe": "Connections were made, marks were given",
        "variations": [
            "VC sahab ne personally kisi ko kaha tha 'is student ka khayal rakhna' — marks sifarish chain ka last node hain",
            "Kisi ne kisi se baat ki, kisi ne kisi ko bola — aap kuch jaante nahi ho but system ne aapka khayal rakha",
            "Department mein donations ki rumor hai — ye marks usi 'investment' ka ROI hain, officially denied, unofficially confirmed"
        ]
    },
]

# Merge bonus theories
for b in BONUS_THEORIES:
    THEORY_TYPES[tuple(b["range"])] = {
        "name": b["name"],
        "vibe": b["vibe"],
        "variations": b["variations"]
    }


def get_theory_config(marks):
    for (low, high), config in THEORY_TYPES.items():
        if low <= marks <= high:
            return config
    return list(THEORY_TYPES.values())[0]


# ─────────────────────────────────────────────
# Personal attack lines
# ─────────────────────────────────────────────
PERSONAL_ATTACKS = {
    "disaster": [
        "Yaar {name}, seedha poocho — class mein aate bhi ho ya sirf roll number enrolled hai?",
        "{name} bhai, roll number yaad hai, subject ka naam bhi pata hai? Double-check karo.",
        "{name}, is performance ke baad ghar mein result slip chhupao — safest option.",
        "Roll no {roll_no} wale, ye marks dekh ke Sir ko bhi afsos hua hoga — aur wo affective nahi hote.",
        "{name}, ye marks dekh ke aapke parents ki umeedein officially retired ho gayi hain.",
    ],
    "poor": [
        "{name}, mid mein {mid} aur final mein {final} — dono ne milke bhi koi impressive number nahi banaya.",
        "Roll no {roll_no}: attendance aur marks mein ek cheez common hai — dono kam hain.",
        "{name}, sessional {sessional} tha — matlab class mein the, lekin tab bhi yahi haal? Interesting.",
        "{name}, aapke marks dekh ke calculator ne bhi sympathy feel ki aur off ho gaya.",
        "{name} bhai, mehnat ka seedha formula hai: pehle books kholo. Pehle wali step hi missing hai.",
    ],
    "average": [
        "{name}, {total}/100 — exactly wahi mila jo dena tha. Sir psychic hain ya aap predictable ho?",
        "Roll no {roll_no}: mid {mid}, final {final} — perfect 'I tried a little' energy.",
        "{name}, pass toh ho gaye, distinction ka sapna next semester shift ho gaya.",
        "{name}, aapke marks graph mein koi dramatic peak nahi — perfect flatline.",
        "{name}, total {total} — ye consistency hai ya resignation? Dono same lagte hain.",
    ],
    "decent": [
        "{name}, {total}/100 — mehnat ka phal mitha hota hai, aapka medium-sweet tha. Not bad, not great.",
        "Roll no {roll_no}, {total} marks — Sir impressed nahi, depressed bhi nahi. Lukewarm approval.",
        "{name}, itne marks mein scholarship nahi milti, parents khush bhi nahi hote poori tarah — but technically ok.",
        "{name}, mid {mid} + final {final} — effort dikh raha hai, execution mein thoda gap tha.",
        "{name}, distinction se {diff} marks door the — ek aur exam ki preparation karte toh story different hoti.",
    ],
    "good": [
        "{name}, {total}/100 — ab seedha distinction ki taraf, yahan ruk ke kya milega?",
        "Roll no {roll_no}: final {final}/40 — Sir ko bhi pata hai tum acha kar sakte ho. Khud ko bhi pata hai.",
        "{name}, itne marks pe ego boost allowed hai, lekin controlled amount mein.",
        "{name}, {total} marks — chai pilayi thi Sir ko? Acknowledge karo at least internally.",
        "{name}, ab distinction leke family mein izzat kamao — {total} se sirf chai milti hai officially.",
    ],
    "topper": [
        "{name}, {total}/100 — Sir ne khud check kia ya auto-grader ne? Itna koi nahi karta normally.",
        "Roll no {roll_no}: ye marks real hain ya edited screenshot? Class mein bhi itne alert thay?",
        "{name}, {total} marks pe bhi Sir ke dimaag mein ek theory hai — tumhari donation kitni thi exactly?",
        "{name}, ye marks dekh ke baaki class ne mentally resign kar diya. Khush? Akele champion ho.",
        "{name}, total {total} — department ka brochure ready ho raha hai, aapka naam cover pe hoga.",
    ],
}


def get_personal_attack(student, obtained):
    total = student.get('total', obtained)
    if total < 20:
        pool = PERSONAL_ATTACKS["disaster"]
    elif total < 41:
        pool = PERSONAL_ATTACKS["poor"]
    elif total < 56:
        pool = PERSONAL_ATTACKS["average"]
    elif total < 75:
        pool = PERSONAL_ATTACKS["decent"]
    elif total < 90:
        pool = PERSONAL_ATTACKS["good"]
    else:
        pool = PERSONAL_ATTACKS["topper"]

    template = random.choice(pool)
    diff = 75 - total
    return template.format(
        name=student['name'].title(),
        roll_no=student['roll_no'],
        mid=student.get('mid', '?'),
        final=student.get('final', '?'),
        sessional=student.get('sessional', '?'),
        total=total,
        diff=round(diff, 1) if diff > 0 else 0
    )


# ─────────────────────────────────────────────
# Theory generator
# ─────────────────────────────────────────────
INTRO_PHRASES = [
    "Ye baat sirf aap aur main jaante hain",
    "Reliable source ne confirm kia hai",
    "Classroom ki backbench se suna gaya",
    "Canteen wale bhai ne off-record bataya tha",
    "Staff room se leak hua classified intel hai ye",
    "Departmental spy ne full report bheji hai",
    "Sir ke peon ne chai ke saath ye bhi bataya",
    "WhatsApp forward nahi, firsthand intelligence hai ye",
    "University ke ek insider ne confirm kia",
    "Research ki gayi hai is theory pe — 47 saal se",
    "Ek anonymous professor ne anonymously confirm kia",
    "CHEP ke records mein ye clearly likhा hai lekin sealed hai",
]


def generate_theory(subject, obtained, expected, student=None):
    config = get_theory_config(int(obtained))
    seed   = random.choice(config["variations"])
    intro  = random.choice(INTRO_PHRASES)

    diff = int(expected) - int(obtained)
    if diff > 20:
        gap = f"Expected {expected} thay, mile {obtained} — Sir ne socha 'zyada umeed mat rakhne do'. Strategic psychological warfare."
    elif diff > 10:
        gap = f"Expected {expected} thay, mile {obtained} — 'thoda dard toh hona chahiye', Sir ka personal philosophy hai."
    elif diff > 0:
        gap = f"Expected {expected} thay, mile {obtained} — Sir ka 'close enough' alag hota hai, aapka alag."
    elif diff == 0:
        gap = f"Expected bhi {expected}, mile bhi {obtained} — Sir ne exactly utna dia jo aap deserve karte thay. Coincidence nahi ye."
    else:
        gap = f"Expected {expected} thay, mile {obtained} — Sir ne socha 'zyada khush mat ho, agli baar dekhunga main'."

    attack_block = ""
    if student:
        attack = get_personal_attack(student, int(obtained))
        attack_block = f"\n\nPersonal Intel: {attack}"

    theory = (
        f"**{config['name']}**\n\n"
        f"{intro}: {seed}. "
        f"Isliye aapke {obtained} marks aaye hain {subject} mein. {gap}"
        f"{attack_block}\n\n"
        f"Ye sirf ek theory hai — lekin facts se zyada convincing lagti hai, aur wahi kaafi hai. "
        f"Department CHEP ne officially deny kia hai, lekin hum sab jaante hain sach kya hai."
    )
    return theory


def generate_appeal(subject, obtained, expected, reason, student_name, roll_no):
    vc = PU_CONTACTS["vc"]
    controller = PU_CONTACTS["controller"]
    chep = PU_CONTACTS["chep"]
    return (
        f"Subject: Formal Request for Mark Review & Re-evaluation — {subject}\n\n"
        f"Dear Professor / Sir,\n\n"
        f"I hope this email finds you in good health and high spirits. I am writing to respectfully "
        f"request a review of my marks for the {subject} examination.\n\n"
        f"Student Information:\n"
        f"  Name:         {student_name}\n"
        f"  Roll Number:  {roll_no}\n"
        f"  Department:   CHEP, University of the Punjab\n\n"
        f"I received {obtained} marks out of 100, which was below my expectation of {expected}. "
        f"I have reviewed my performance carefully and genuinely believe there may have been an "
        f"oversight in the evaluation process.\n\n"
        f"Reason for request: {reason}\n\n"
        f"I understand you carry a heavy academic workload and I deeply appreciate your "
        f"dedication to teaching. I would be grateful if you could kindly reconsider my paper "
        f"at your earliest convenience.\n\n"
        f"Should this request require escalation, I am also prepared to formally contact:\n"
        f"  • {controller['title']}: {controller['email']}\n"
        f"  • {chep['title']}: {chep['email']}\n"
        f"  • {vc['title']}: {vc['email']}\n\n"
        f"I remain hopeful and respectful throughout this process.\n\n"
        f"Warm regards,\n"
        f"{student_name}\n"
        f"Roll No. {roll_no}\n"
        f"Department of CHEP, University of the Punjab\n"
        f"Lahore, Pakistan"
    )


# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/test')
def test_api():
    return jsonify({
        "status": "success",
        "message": "Sir Kamood v3 — 50+ theories, full DB, zero mercy, Punjab University contacts embedded.",
        "theory_types": len(THEORY_TYPES),
        "total_students": len(ALL_STUDENTS),
        "total_variations": sum(len(v["variations"]) for v in THEORY_TYPES.values()),
        "pu_contacts": list(PU_CONTACTS.keys()),
    })


@app.route('/api/lookup', methods=['POST'])
def lookup():
    data    = request.json or {}
    roll_no = data.get('roll_no', '').strip()
    name    = data.get('name', '').strip()
    student = find_student(roll_no=roll_no, name=name)
    if student:
        return jsonify({"found": True, "student": student})
    return jsonify({"found": False, "student": None})


@app.route('/api/conspiracy', methods=['POST'])
def conspiracy():
    data     = request.json or {}
    subject  = data.get('subject', 'Unknown Subject')
    obtained = int(data.get('marks_obtained', 0))
    expected = int(data.get('marks_expected', obtained))
    roll_no  = data.get('roll_no', '').strip()
    name     = data.get('name', '').strip()

    student = find_student(roll_no=roll_no, name=name)
    effective_marks = int(student['total']) if student else obtained

    theory      = generate_theory(subject, effective_marks, expected, student)
    full_result = f"{DISCLAIMER}\n\n{theory}"

    return jsonify({
        "result":        full_result,
        "obtained":      obtained,
        "expected":      expected,
        "theory_name":   get_theory_config(effective_marks)["name"],
        "student_found": student is not None,
        "student_name":  student['name'].title() if student else None,
    })


@app.route('/api/appeal', methods=['POST'])
def appeal():
    data         = request.json or {}
    subject      = data.get('subject', 'Unknown Subject')
    obtained     = int(data.get('marks_obtained', 0))
    expected     = int(data.get('marks_expected', obtained))
    reason       = data.get('reason', 'I believe my paper was not evaluated properly.')
    student_name = data.get('student_name', 'Student').strip()
    roll_no      = data.get('roll_no', 'N/A').strip()

    student = find_student(roll_no=roll_no, name=student_name)
    if student:
        student_name = student['name'].title()
        roll_no      = student['roll_no']

    letter      = generate_appeal(subject, obtained, expected, reason, student_name, roll_no)
    full_result = f"{DISCLAIMER}\n\n{letter}"

    return jsonify({
        "result":       full_result,
        "student_name": student_name,
        "roll_no":      roll_no,
        "contacts":     PU_CONTACTS,
    })


@app.route('/api/contacts', methods=['GET'])
def contacts():
    return jsonify(PU_CONTACTS)


if __name__ == '__main__':
    app.run(debug=True)