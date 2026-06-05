import os
import json
import random
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "meta-llama/llama-3.1-8b-instruct:free"

DISCLAIMER = "Disclaimer: This is purely for fun and entertainment purposes. No hate or disrespect intended towards any professor, department, or institution. Sab moh maya hai."

# 20 marks ranges with different vibes
THEORY_TYPES = {
    # FAIL RANGE (0-49)
    (0, 9): {
        "name": "Extreme Disaster",
        "vibe": "Sir literally had the worst day of his life. Everything went wrong. Generate ONE extreme theory about Sir's life completely falling apart.",
        "sub_variations": [
            "Sir ki biwi ne ghar se nikaal diya tha, wo depression mein paper check kia",
            "Sir ka phone chori ho gaya tha, usi ghusay mein marks diye",
            "Sir ne subah se kuch nahi khaya tha, hangry marking",
            "Sir ki nayi bike ka accident ho gaya tha, poora ghusa aap pe nikaala",
            "Sir ne lottery ticket kharidi thi, nahi nikli, aapka paper usi din check hua"
        ]
    },
    (10, 19): {
        "name": "Biwi Ka Badla",
        "vibe": "Sir's wife destroyed him. Generate ONE theory about biwi se maar padi and the aftermath on your marks.",
        "sub_variations": [
            "Biwi ne jootay maare thay kal raat, Sir ne aapke marks pe revenge lia",
            "Biwi ne kaha tha 'tum kuch nahi kar sakte', Sir ne prove kia aapke marks se",
            "Biwi ne ghar ka kaam Sir pe chhod diya tha, Sir ne ghusa paper mein nikaala",
            "Biwi ne Sir ka phone check kia tha, uske baad ka mood aapke marks mein dikh raha hai",
            "Biwi ne Sir se keh diya 'mere abba se kum ho tum', Sir ne ego satisfy kia"
        ]
    },
    (20, 29): {
        "name": "Petrol Price Trauma",
        "vibe": "Sir went to fill petrol and saw the price. Generate ONE theory about economic depression affecting your marks.",
        "sub_variations": [
            "Petrol 300+ ho gaya tha, Sir ne socha fail karna hi best investment hai",
            "Sir ne CNG dalwai thi, line mein 2 ghante lag gaye, wo ghusa aapke marks mein",
            "Sir ne socha tha bike se jaunga, petrol dekh ke paidal aaye, poora din kharab tha",
            "Sir ne EMI aur petrol dono calculate kiye, depression mein paper check kia",
            "Sir ne socha tha ke 'aaj sasta petrol mila hai', phir pata chala wo kerosene tha"
        ]
    },
    (30, 39): {
        "name": "Cricket Match Curse",
        "vibe": "Sir's cricket team lost badly. Generate ONE theory about cricket trauma destroying your marks.",
        "sub_variations": [
            "India ne Pakistan ko haraya tha, Sir ne ghusa aapke paper pe nikaala",
            "Sir ne match pe bet lagayi thi, haar gaye, aapke marks usi ka hisaab",
            "Sir ka favorite player out ho gaya first ball pe, wo mood aapke marks mein hai",
            "Sir ne socha tha match dekh ke relax karunga, rain ne washout kar diya",
            "Sir ne stadium tickets kharidi thi, match postpone ho gaya, poora paisa zaya"
        ]
    },
    (40, 49): {
        "name": "Chai Mein Cheeni Kam",
        "vibe": "Sir's morning chai was ruined. Generate ONE theory about chai disaster leading to mark disaster.",
        "sub_variations": [
            "Chai mein cheeni nahi thi, Sir ne pure din ki narazgi aapke marks pe nikaali",
            "Sir ne chai garam mangi thi, thandi milli, wo ghusa abhi tak tha",
            "Chai wale ne doodh kam daala tha, Sir ne socha 'main bhi kam marks dunga'",
            "Sir ne green tea try ki thi, usi depression mein paper check kia",
            "Chai wala aaj chutti pe tha, Sir ne substitute coffee pee, usi ka asar"
        ]
    },
    
    # AVERAGE RANGE (50-64)
    (50, 54): {
        "name": "Neend Poori Nahi Hui",
        "vibe": "Sir barely slept. Generate ONE theory about sleepy Sir checking papers half-conscious.",
        "sub_variations": [
            "Sir raat ko 3 baje soye thay, subah 8 baje uth ke paper check kia, neend mein marks diye",
            "Sir ne socha tha 'bas 5 minute ka nap', 2 ghante nikal gaye, jaldi mein marks diye",
            "Sir ke bachay ne raat ko roka tha, Sir ne neend mein paper check kia",
            "Sir ne energy drink pee thi, crash ho gaya, neend mein marking ki",
            "Sir ne socha tha ke 'aaj jaldi khatam karunga', neend ne khatam kar diya"
        ]
    },
    (55, 59): {
        "name": "WhatsApp Distraction",
        "vibe": "Sir was busy on WhatsApp family groups. Generate ONE theory about phone addiction affecting marks.",
        "sub_variations": [
            "Family group pe larai chal rahi thi, Sir ne ghusay mein random marks daal diye",
            "Sir ne crush ka message aaya tha, khushi mein zyada marks de diye, phir realize hua",
            "Sir ne WhatsApp status dekh ke depression mein chale gaye, marks pe asar hua",
            "Sir ne forwarded message padha tha 'marks are just numbers', usi ne inspire kia",
            "Sir ne voice note suna tha biwi ka, 5 minute ke baad marks daalne lage"
        ]
    },
    (60, 64): {
        "name": "Lunch Break Pe Tha",
        "vibe": "Sir was hungry and rushing to lunch. Generate ONE theory about food desperation affecting marks.",
        "sub_variations": [
            "Sir ne biryani ka order diya tha, jaldi mein paper check kia, marks average aaye",
            "Canteen mein biryani khatam hone wali thi, Sir ne jaldi jaldi marks diye",
            "Sir ne socha tha 'bas ye last paper', canteen band hone se pehle pahunchna tha",
            "Sir ne lunch skip kia tha, bhooke pet marking ki, mercy marks diye",
            "Sir ne daal chawal kha ke aaye thay, satisfaction mein average marks diye"
        ]
    },
    
    # GOOD RANGE (65-79)
    (65, 69): {
        "name": "Biryani Wali Khushi",
        "vibe": "Sir had amazing biryani. Generate ONE theory about food happiness boosting marks.",
        "sub_variations": [
            "Biwi ne aaj special biryani banayi thi, Sir ka mood itna acha tha ke achay marks diye",
            "Sir ne canteen se double masala biryani khai thi, khushi mein marks badh gaye",
            "Biryani mein extra aloo mile thay Sir ko, wo khushi aapke marks mein dikh rahi hai",
            "Sir ne socha tha 'aaj diet karunga', phir biryani dekh ke plan cancel, khushi se marks diye",
            "Biryani ka order late aaya tha, lekin taste acha tha, Sir ne positive marking ki"
        ]
    },
    (70, 74): {
        "name": "Cricket Jeet Gaya",
        "vibe": "Sir's team won the match. Generate ONE theory about cricket victory happiness.",
        "sub_variations": [
            "Pakistan ne match jeet liya tha, Sir ne khushi mein achay marks diye sabko",
            "Sir ne bet jeet li thi, usi khushi mein paper check kia, sabke marks achay aaye",
            "Sir ka favorite player century mar gaya tha, wo excitement aapke marks mein hai",
            "Sir ne last over mein match jeeta tha, wo adrenaline aapke marks boost ki",
            "Sir ne stadium mein match dekha tha, team jeeti, next day sabko pass kia"
        ]
    },
    (75, 79): {
        "name": "Sunday Ka Mood",
        "vibe": "Sir feels like it's Sunday on a weekday. Generate ONE theory about weekend vibes boosting marks.",
        "sub_variations": [
            "Sir ne socha tha aaj Sunday hai, accidentally Monday pe bhi Sunday ka mood tha",
            "Sir ne weekend plan kia tha, usi khushi mein Tuesday ko Sunday samajh ke marks diye",
            "Sir ne Friday ka mood Monday pe laaya tha, casual marking ki",
            "Sir ne socha tha 'bas 2 din aur weekend hai', usi excitement mein achay marks diye",
            "Sir ne Saturday ki party yaad kar ke paper check kia, hangover khushi mein convert hui"
        ]
    },
    
    # EXCELLENT RANGE (80-100)
    (80, 84): {
        "name": "Chai Pilayi Thi",
        "vibe": "Student brought Sir chai. Generate ONE theory about chai bribery and favoritism.",
        "sub_variations": [
            "Aap ne Sir ko special elaichi chai pilayi thi, usi ka badla {marks} marks mein mila",
            "Chai mein extra cheeni daali thi aap ne, Sir ne sweetness marks mein convert ki",
            "Aap ne chai ke saath biscuits bhi diye thay, combo deal pe bonus marks mile",
            "Sir ne aapki chai ki tareef ki thi class mein, favoritism officially announce ho gaya",
            "Aap ne garam garam chai di thi thand mein, Sir ne dil se marks diye"
        ]
    },
    (85, 89): {
        "name": "Favorite Student Theory",
        "vibe": "You are clearly Sir's favorite. Generate ONE theory about extreme teacher's pet favoritism.",
        "sub_variations": [
            "Sir ne aapko apne bete jaisa samajh lia hai, beta jitne marks milte hain utne diye",
            "Aap ne Sir ki car wash ki thi last week, usi ka return on investment ye marks hain",
            "Sir ne aapka naam class mein 'meri ankh ka taara' kaha tha, officially favorite ho",
            "Aap ne Sir ke bachay ki tuition free ki thi, usi ka shukriya ye marks hain",
            "Sir ne aapki project report copy-paste ki thi apni research mein, co-author marks diye"
        ]
    },
    (90, 94): {
        "name": "Sir Ne Khud Solve Kia",
        "vibe": "Sir solved the paper himself for you. Generate ONE theory about Sir doing the work.",
        "sub_variations": [
            "Sir ne aapke paper pe khud answers likhe thay, aap toh exam mein soo rahe thay",
            "Sir ne socha tha 'ye student toh mera future successor hai', khud paper solve kia",
            "Sir ne aapki jagah exam diya tha, obviously {marks} aaye hain",
            "Sir ne aapke answers ko 'improve' kia tha checking ke waqt, red pen se green kar diye",
            "Sir ne aapki copy pe 'excellent' likhne se pehle khud verify kia tha, full marks bante hain"
        ]
    },
    (95, 100): {
        "name": "University Ka Future Star",
        "vibe": "You are the chosen one. Generate ONE theory about you being the university's golden child.",
        "sub_variations": [
            "VC sahab ne personally order kia tha ke is student ko top karna hai, {marks} minimum hain",
            "University ne aapko brand ambassador choose kia tha, {marks} toh publicity stunt hain",
            "Sir ne socha tha 'ye toh next VC banega', usi ne marks set kiye hain",
            "Aap ke papa ne donation di thi, {marks} usi ka receipt hain",
            "Sir ne aapki photo university brochure ke liye mangi thi, {marks} modeling fees hain"
        ]
    }
}

def get_theory_type(marks):
    """Find the right theory type based on marks"""
    for (low, high), config in THEORY_TYPES.items():
        if low <= marks <= high:
            return config
    return THEORY_TYPES[(0, 9)]  # default fallback

def call_openrouter(system_prompt, user_prompt):
    if not OPENROUTER_API_KEY:
        return None
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://sir-kamood.vercel.app",
        "X-Title": "Sir Kamood"
    }
    
    data = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.98,
        "max_tokens": 400,
        "top_p": 0.95,
        "seed": random.randint(1, 99999999)
    }
    
    try:
        resp = requests.post(OPENROUTER_URL, headers=headers, json=data, timeout=45)
        if resp.status_code == 200:
            result = resp.json()
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
        return None
    except Exception:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/test')
def test_api():
    if not OPENROUTER_API_KEY:
        return jsonify({"status": "error", "message": "No OPENROUTER_API_KEY found"})
    
    test = call_openrouter(
        "You are a test assistant. Reply in exactly 5 words.",
        "Say OpenRouter is working."
    )
    
    if test:
        return jsonify({"status": "success", "message": "OpenRouter is working!", "response": test})
    
    return jsonify({"status": "error", "message": "OpenRouter failed. Check your key."})

@app.route('/api/conspiracy', methods=['POST'])
def conspiracy():
    data = request.json
    subject = data.get('subject', 'Unknown Subject')
    obtained = int(data.get('marks_obtained', 0))
    expected = int(data.get('marks_expected', 0))
    
    # Get theory config based on marks
    theory_config = get_theory_type(obtained)
    
    # Pick random sub-variation
    sub_variation = random.choice(theory_config["sub_variations"])
    
    # Build prompts for AI
    system_prompt = f"""You are a hilarious Pakistani university student who roasts professors. {theory_config["vibe"]} Mix Urdu-English (Roman Urdu). 3-4 sentences max. No emojis. Be creative and different every time. Title it with a bold heading like **{theory_config["name"]}**."""
    
    user_prompt = f"""Student got {obtained} out of 100 in {subject}, expected {expected}. 

Here is a seed idea for your theory (you can expand on it creatively): {sub_variation}

Generate ONE unique, funny theory. Make it personal and specific to this student's situation. Title it with **{theory_config["name"]}**."""
    
    # Call AI
    result = call_openrouter(system_prompt, user_prompt)
    
    # Fallback if API fails
    if not result:
        result = f"""**{theory_config["name"]}**\n\n{sub_variation}. Isliye aapke {obtained} marks banaye hain. Expected thay {expected}, lekin yehi haalat thi. Kismat ka khel hai, bhai."""
    
    # Add disclaimer
    full_result = f"{DISCLAIMER}\n\n{result}"
    
    return jsonify({
        "result": full_result, 
        "obtained": obtained, 
        "expected": expected,
        "theory_name": theory_config["name"]
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
    
    system_prompt = "You are a professional email writer. Write a polite, formal appeal letter to a professor requesting mark review. Tone: respectful but firm. No emojis. Professional formatting."
    
    user_prompt = f"""Write a formal email to a professor.

Student: {student_name}, Roll No: {roll_no}, Department: CHEP
Subject: {subject}
Marks obtained: {obtained}/100
Expected: {expected}
Reason: {reason}

Requirements:
- Start with "Subject: Request for Mark Review - {subject}"
- Include student info (Name, Roll No, Department: CHEP)
- Professional tone, not entitled
- Sign off as "{student_name}, Roll No. {roll_no}, Department of CHEP"
- 4-5 paragraphs max"""
    
    result = call_openrouter(system_prompt, user_prompt)
    
    if not result:
        result = f"""Subject: Request for Mark Review - {subject}

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
    
    full_result = f"{DISCLAIMER}\n\n{result}"
    
    return jsonify({
        "result": full_result, 
        "student_name": student_name, 
        "roll_no": roll_no
    })

if __name__ == '__main__':
    app.run(debug=True)