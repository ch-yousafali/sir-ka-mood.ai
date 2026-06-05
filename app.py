import os
import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

DISCLAIMER = "Disclaimer: This is purely for fun and entertainment purposes. No hate or disrespect intended towards any professor, department, or institution. Sab moh maya hai."

# 15 marks ranges with 5 sub-variations each = 75 unique theory directions
THEORY_TYPES = {
    (0, 9): {
        "name": "Extreme Disaster",
        "vibe": "Sir literally had the worst day of his life",
        "variations": [
            "Sir ki biwi ne ghar se nikaal diya tha, wo depression mein paper check kia",
            "Sir ka phone chori ho gaya tha, usi ghusay mein marks diye",
            "Sir ne subah se kuch nahi khaya tha, hangry marking",
            "Sir ki nayi bike ka accident ho gaya tha, poora ghusa aap pe nikaala",
            "Sir ne lottery ticket kharidi thi, nahi nikli, aapka paper usi din check hua"
        ]
    },
    (10, 19): {
        "name": "Biwi Ka Badla",
        "vibe": "Sir's wife destroyed him",
        "variations": [
            "Biwi ne jootay maare thay kal raat, Sir ne aapke marks pe revenge lia",
            "Biwi ne kaha tha 'tum kuch nahi kar sakte', Sir ne prove kia aapke marks se",
            "Biwi ne ghar ka kaam Sir pe chhod diya tha, Sir ne ghusa paper mein nikaala",
            "Biwi ne Sir ka phone check kia tha, uske baad ka mood aapke marks mein dikh raha hai",
            "Biwi ne Sir se keh diya 'mere abba se kum ho tum', Sir ne ego satisfy kia"
        ]
    },
    (20, 29): {
        "name": "Petrol Price Trauma",
        "vibe": "Sir went to fill petrol and saw the price",
        "variations": [
            "Petrol 300+ ho gaya tha, Sir ne socha fail karna hi best investment hai",
            "Sir ne CNG dalwai thi, line mein 2 ghante lag gaye, wo ghusa aapke marks mein",
            "Sir ne socha tha bike se jaunga, petrol dekh ke paidal aaye, poora din kharab tha",
            "Sir ne EMI aur petrol dono calculate kiye, depression mein paper check kia",
            "Sir ne socha tha ke 'aaj sasta petrol mila hai', phir pata chala wo kerosene tha"
        ]
    },
    (30, 39): {
        "name": "Cricket Match Curse",
        "vibe": "Sir's cricket team lost badly",
        "variations": [
            "India ne Pakistan ko haraya tha, Sir ne ghusa aapke paper pe nikaala",
            "Sir ne match pe bet lagayi thi, haar gaye, aapke marks usi ka hisaab",
            "Sir ka favorite player out ho gaya first ball pe, wo mood aapke marks mein hai",
            "Sir ne socha tha match dekh ke relax karunga, rain ne washout kar diya",
            "Sir ne stadium tickets kharidi thi, match postpone ho gaya, poora paisa zaya"
        ]
    },
    (40, 49): {
        "name": "Chai Mein Cheeni Kam",
        "vibe": "Sir's morning chai was ruined",
        "variations": [
            "Chai mein cheeni nahi thi, Sir ne pure din ki narazgi aapke marks pe nikaali",
            "Sir ne chai garam mangi thi, thandi milli, wo ghusa abhi tak tha",
            "Chai wale ne doodh kam daala tha, Sir ne socha 'main bhi kam marks dunga'",
            "Sir ne green tea try ki thi, usi depression mein paper check kia",
            "Chai wala aaj chutti pe tha, Sir ne substitute coffee pee, usi ka asar"
        ]
    },
    (50, 54): {
        "name": "Neend Poori Nahi Hui",
        "vibe": "Sir barely slept",
        "variations": [
            "Sir raat ko 3 baje soye thay, subah 8 baje uth ke paper check kia, neend mein marks diye",
            "Sir ne socha tha 'bas 5 minute ka nap', 2 ghante nikal gaye, jaldi mein marks diye",
            "Sir ke bachay ne raat ko roka tha, Sir ne neend mein paper check kia",
            "Sir ne energy drink pee thi, crash ho gaya, neend mein marking ki",
            "Sir ne socha tha ke 'aaj jaldi khatam karunga', neend ne khatam kar diya"
        ]
    },
    (55, 59): {
        "name": "WhatsApp Distraction",
        "vibe": "Sir was busy on WhatsApp",
        "variations": [
            "Family group pe larai chal rahi thi, Sir ne ghusay mein random marks daal diye",
            "Sir ne crush ka message aaya tha, khushi mein zyada marks de diye, phir realize hua",
            "Sir ne WhatsApp status dekh ke depression mein chale gaye, marks pe asar hua",
            "Sir ne forwarded message padha tha 'marks are just numbers', usi ne inspire kia",
            "Sir ne voice note suna tha biwi ka, 5 minute ke baad marks daalne lage"
        ]
    },
    (60, 64): {
        "name": "Lunch Break Pe Tha",
        "vibe": "Sir was hungry and rushing",
        "variations": [
            "Sir ne biryani ka order diya tha, jaldi mein paper check kia, marks average aaye",
            "Canteen mein biryani khatam hone wali thi, Sir ne jaldi jaldi marks diye",
            "Sir ne socha tha 'bas ye last paper', canteen band hone se pehle pahunchna tha",
            "Sir ne lunch skip kia tha, bhooke pet marking ki, mercy marks diye",
            "Sir ne daal chawal kha ke aaye thay, satisfaction mein average marks diye"
        ]
    },
    (65, 69): {
        "name": "Biryani Wali Khushi",
        "vibe": "Sir had amazing biryani",
        "variations": [
            "Biwi ne aaj special biryani banayi thi, Sir ka mood itna acha tha ke achay marks diye",
            "Sir ne canteen se double masala biryani khai thi, khushi mein marks badh gaye",
            "Biryani mein extra aloo mile thay Sir ko, wo khushi aapke marks mein dikh rahi hai",
            "Sir ne socha tha 'aaj diet karunga', phir biryani dekh ke plan cancel, khushi se marks diye",
            "Biryani ka order late aaya tha, lekin taste acha tha, Sir ne positive marking ki"
        ]
    },
    (70, 74): {
        "name": "Cricket Jeet Gaya",
        "vibe": "Sir's team won the match",
        "variations": [
            "Pakistan ne match jeet liya tha, Sir ne khushi mein achay marks diye sabko",
            "Sir ne bet jeet li thi, usi khushi mein paper check kia, sabke marks achay aaye",
            "Sir ka favorite player century mar gaya tha, wo excitement aapke marks mein hai",
            "Sir ne last over mein match jeeta tha, wo adrenaline aapke marks boost ki",
            "Sir ne stadium mein match dekha tha, team jeeti, next day sabko pass kia"
        ]
    },
    (75, 79): {
        "name": "Sunday Ka Mood",
        "vibe": "Sir feels like it's Sunday",
        "variations": [
            "Sir ne socha tha aaj Sunday hai, accidentally Monday pe bhi Sunday ka mood tha",
            "Sir ne weekend plan kia tha, usi khushi mein Tuesday ko Sunday samajh ke marks diye",
            "Sir ne Friday ka mood Monday pe laaya tha, casual marking ki",
            "Sir ne socha tha 'bas 2 din aur weekend hai', usi excitement mein achay marks diye",
            "Sir ne Saturday ki party yaad kar ke paper check kia, hangover khushi mein convert hui"
        ]
    },
    (80, 84): {
        "name": "Chai Pilayi Thi",
        "vibe": "Student brought Sir chai",
        "variations": [
            "Aap ne Sir ko special elaichi chai pilayi thi, usi ka badla marks mein mila",
            "Chai mein extra cheeni daali thi aap ne, Sir ne sweetness marks mein convert ki",
            "Aap ne chai ke saath biscuits bhi diye thay, combo deal pe bonus marks mile",
            "Sir ne aapki chai ki tareef ki thi class mein, favoritism officially announce ho gaya",
            "Aap ne garam garam chai di thi thand mein, Sir ne dil se marks diye"
        ]
    },
    (85, 89): {
        "name": "Favorite Student Theory",
        "vibe": "You are clearly Sir's favorite",
        "variations": [
            "Sir ne aapko apne bete jaisa samajh lia hai, beta jitne marks milte hain utne diye",
            "Aap ne Sir ki car wash ki thi last week, usi ka return on investment ye marks hain",
            "Sir ne aapka naam class mein 'meri ankh ka taara' kaha tha, officially favorite ho",
            "Aap ne Sir ke bachay ki tuition free ki thi, usi ka shukriya ye marks hain",
            "Sir ne aapki project report copy-paste ki thi apni research mein, co-author marks diye"
        ]
    },
    (90, 94): {
        "name": "Sir Ne Khud Solve Kia",
        "vibe": "Sir solved the paper himself",
        "variations": [
            "Sir ne aapke paper pe khud answers likhe thay, aap toh exam mein soo rahe thay",
            "Sir ne socha tha 'ye student toh mera future successor hai', khud paper solve kia",
            "Sir ne aapki jagah exam diya tha, obviously full marks aaye hain",
            "Sir ne aapke answers ko 'improve' kia tha checking ke waqt, red pen se green kar diye",
            "Sir ne aapki copy pe 'excellent' likhne se pehle khud verify kia tha, full marks bante hain"
        ]
    },
    (95, 100): {
        "name": "University Ka Future Star",
        "vibe": "You are the chosen one",
        "variations": [
            "VC sahab ne personally order kia tha ke is student ko top karna hai, ye marks minimum hain",
            "University ne aapko brand ambassador choose kia tha, ye marks toh publicity stunt hain",
            "Sir ne socha tha 'ye toh next VC banega', usi ne marks set kiye hain",
            "Aap ke papa ne donation di thi, ye marks usi ka receipt hain",
            "Sir ne aapki photo university brochure ke liye mangi thi, ye marks modeling fees hain"
        ]
    }
}

def get_theory_config(marks):
    """Find the right theory config based on marks"""
    for (low, high), config in THEORY_TYPES.items():
        if low <= marks <= high:
            return config
    return THEORY_TYPES[(0, 9)]

def generate_theory(subject, obtained, expected):
    """Generate a complete, creative conspiracy theory"""
    config = get_theory_config(obtained)
    seed = random.choice(config["variations"])
    
    # Build a full narrative around the seed
    intro_phrases = [
        "Ye baat sirf aap aur main jaante hain",
        "Source ne confirm kia hai",
        "Classroom ki backbench se suna gaya hai",
        "Canteen wale bhai ne bataya tha",
        "Staff room se leak hua intel hai"
    ]
    
    intro = random.choice(intro_phrases)
    
    # Add some random flavor based on marks difference
    diff = expected - obtained
    if diff > 20:
        extra = f" Expected thay {expected}, lekin {obtained} isliye diye ke Sir ne socha 'zyada hope mat de isko'. Ye strategic failure tha."
    elif diff > 10:
        extra = f" Expected {expected} thay, lekin Sir ne {obtained} diye ke 'thoda dard toh hona chahiye'. Ye controlled damage tha."
    elif diff > 0:
        extra = f" Expected {expected} thay, lekin Sir ne {obtained} diye ke 'close enough'. Ye Sir ka version of 'almost there' tha."
    elif diff <= 0:
        extra = f" Expected {expected} thay, lekin {obtained} mil gaye. Sir ne socha 'zyada hi acha kar lia, next time tough dunga'."
    else:
        extra = ""
    
    # Build the full theory
    theory = f"""**{config["name"]}**

{intro}: {seed}. Isliye aapke {obtained} marks banaye hain {subject} mein.{extra}

Ye sirf ek theory hai, lekin facts se zyada convincing lagti hai. Department CHEP ne officially deny kia hai, lekin hum jaante hain ke sach kya hai."""
    
    return theory

def generate_appeal(subject, obtained, expected, reason, student_name, roll_no):
    """Generate a formal appeal letter"""
    return f"""Subject: Request for Mark Review - {subject}

Dear Professor,

I hope this email finds you well. I am writing to respectfully request a review of my marks for the {subject} examination.

Student Information:
- Name: {student_name}
- Roll Number: {roll_no}
- Department: CHEP

I received {obtained} marks out of 100, which was significantly lower than my expectation of {expected}. I have carefully reviewed my preparation and performance, and I believe there may have been an oversight in the evaluation process.

My reason for this request is as follows: {reason}

I understand that you have a heavy workload and I truly appreciate the time and effort you dedicate to teaching. However, I would be grateful if you could kindly reconsider my paper at your earliest convenience.

Thank you for your understanding and support.

{student_name}
Roll No. {roll_no}
Department of CHEP"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/test')
def test_api():
    return jsonify({
        "status": "success",
        "message": "Sir Kamood is running 100% offline — no API needed!",
        "mode": "local_ai",
        "theory_types": len(THEORY_TYPES),
        "total_variations": sum(len(v["variations"]) for v in THEORY_TYPES.values())
    })

@app.route('/api/conspiracy', methods=['POST'])
def conspiracy():
    data = request.json
    subject = data.get('subject', 'Unknown Subject')
    obtained = int(data.get('marks_obtained', 0))
    expected = int(data.get('marks_expected', 0))
    
    theory = generate_theory(subject, obtained, expected)
    full_result = f"{DISCLAIMER}\n\n{theory}"
    
    return jsonify({
        "result": full_result,
        "obtained": obtained,
        "expected": expected,
        "theory_name": get_theory_config(obtained)["name"]
    })

@app.route('/api/appeal', methods=['POST'])
def appeal():
    data = request.json
    subject = data.get('subject', 'Unknown Subject')
    obtained = int(data.get('marks_obtained', 0))
    expected = int(data.get('marks_expected', 0))
    reason = data.get('reason', 'I believe my paper was not evaluated properly')
    student_name = data.get('student_name', 'Yousuf Ali')
    roll_no = data.get('roll_no', '1123BE')
    
    letter = generate_appeal(subject, obtained, expected, reason, student_name, roll_no)
    full_result = f"{DISCLAIMER}\n\n{letter}"
    
    return jsonify({
        "result": full_result,
        "student_name": student_name,
        "roll_no": roll_no
    })

if __name__ == '__main__':
    app.run(debug=True)