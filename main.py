import streamlit as st

# ==========================================
# 1. 페이지 기본 설정 및 디자인 (CSS)
# ==========================================
st.set_page_config(
    page_title="나의 MBTI 단짝 포켓몬 찾기",
    page_icon="⚡",
    layout="centered"
)

# 따뜻한 크림 & 노란색 톤 스타일 적용 (큰 글씨, 직관적인 디자인)
st.markdown("""
    <style>
    /* 전체 배경을 따뜻한 크림색으로 설정 */
    .stApp {
        background-color: #FFFDF0;
        font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
    }
    
    /* 타이틀 영역 스타일 */
    .title-header {
        background-color: #FEF3C7;
        padding: 24px 16px;
        border-radius: 20px;
        text-align: center;
        border: 3px solid #FCD34D;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.15);
        margin-bottom: 25px;
    }
    
    .main-title {
        color: #92400E;
        font-size: 2.2rem !important;
        font-weight: 800;
        margin-bottom: 8px;
    }
    
    .sub-title {
        color: #B45309;
        font-size: 1.2rem !important;
        font-weight: 500;
    }

    /* 포켓몬 결과 카드 스타일 */
    .result-card {
        background-color: #FFFFFF;
        border: 3px solid #F59E0B;
        border-radius: 24px;
        padding: 28px;
        box-shadow: 0 8px 20px rgba(217, 119, 6, 0.12);
        margin-top: 20px;
        text-align: center;
    }

    .pokemon-name {
        color: #78350F;
        font-size: 2rem !important;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .pokemon-english {
        color: #D97706;
        font-size: 1.1rem !important;
        font-weight: 600;
        margin-bottom: 12px;
    }

    .type-badge {
        display: inline-block;
        background-color: #FEF3C7;
        color: #92400E;
        padding: 6px 18px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 1.1rem !important;
        border: 1.5px solid #FCD34D;
        margin-bottom: 16px;
    }

    .info-box {
        background-color: #FFFBEB;
        border-left: 5px solid #F59E0B;
        border-radius: 12px;
        padding: 16px 20px;
        text-align: left;
        margin-top: 15px;
        color: #451A03;
        font-size: 1.1rem !important;
        line-height: 1.7;
    }

    .info-title {
        color: #B45309;
        font-weight: 800;
        font-size: 1.15rem !important;
        margin-bottom: 6px;
    }

    /* 버튼 스타일 커스텀 */
    div.stButton > button {
        background-color: #F59E0B !important;
        color: #FFFFFF !important;
        font-size: 1.3rem !important;
        font-weight: bold !important;
        border-radius: 16px !important;
        padding: 12px 28px !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(245, 158, 11, 0.3) !important;
        transition: all 0.2s ease-in-out;
        width: 100%;
    }

    div.stButton > button:hover {
        background-color: #D97706 !important;
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 16가지 MBTI & 포켓몬 매핑 데이터
# ==========================================
POKEMON_MBTI_DATA = {
    "ISTJ": {
        "mbti_desc": "청렴결백한 논리주의자",
        "name_kr": "거북왕",
        "name_en": "Blastoise",
        "type": "💧 물 타입",
        "img_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/9.png",
        "traits": "묵묵히 책임을 다하며 단단한 방어력과 신뢰감을 주는 든든한 리더",
        "reason": "원칙을 중요시하고 신중한 ISTJ에게 거북왕의 변함없는 든든함과 안정감이 최고의 신뢰를 형성합니다.\n서로의 등 뒤를 안심하고 맡길 수 있는 완벽한 라이프 파트너입니다."
    },
    "ISFJ": {
        "mbti_desc": "용감한 수호자",
        "name_kr": "해피너스",
        "name_en": "Blissey",
        "type": "⚪ 노말 타입",
        "img_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/242.png",
        "traits": "따뜻하고 배려심 깊으며 타인의 상처를 치유하는 온화한 다정함",
        "reason": "헌신적이고 주변 사람을 살뜰히 돌보는 ISFJ의 고운 마음씨와 해피너스의 무한한 애정이 깊은 위로를 줍니다.\n서로를 온전히 보듬어 주는 따뜻한 힐링 조화입니다."
    },
    "INFJ": {
        "mbti_desc": "선의의 옹호자",
        "name_kr": "가디안",
        "name_en": "Gardevoir",
        "type": "🔮 초능력 / ✨ 페어리",
        "img_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/282.png",
        "traits": "깊은 공감 능력과 직관력을 가졌으며 파트너를 지키기 위해서라면 모든 힘을 다함",
        "reason": "조용하지만 확고한 신념과 깊은 감성을 지닌 INFJ의 마음을 가디안은 섬세하게 이해하고 교감합니다.\n영혼의 깊이가 통하는 운명적인 단짝입니다."
    },
    "INTJ": {
        "mbti_desc": "용의주도한 전략가",
        "name_kr": "뮤츠",
        "name_en": "Mewtwo",
        "type": "🔮 초능력 타입",
        "img_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/150.png",
        "traits": "명석한 두뇌, 압도적인 통찰력, 고독하지만 확고한 지적 목표 추진력",
        "reason": "독립적이고 전략적인 INTJ의 통찰력과 뮤츠의 차가우면서도 명석한 머리가 완벽하게 맞아떨어집니다.\n지적이고 탁월한 판단력으로 함께 원대한 비전을 그려나갑니다."
    },
    "ISTP": {
        "mbti_desc": "만능 재주꾼",
        "name_kr": "루카리오",
        "name_en": "Lucario",
        "type": "🥊 격투 / ⚙️ 강철",
        "img_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/448.png",
        "traits": "침착한 상황 판단, 예리한 파동 감각, 실용적인 문제 해결 능력",
        "reason": "말보다 행동으로 솔루션을 찾는 ISTP와 파동을 읽어 즉각 판단하는 루카리오는 최고의 호흡을 과시합니다.\n어떤 위기 상황도 불평 없이 단숨에 해결하는 액션 콤비입니다."
    },
    "ISFP": {
        "mbti_desc": "호기심 많은 예술가",
        "name_kr": "이브이",
        "name_en": "Eevee",
        "type": "⚪ 노말 타입",
        "img_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/133.png",
        "traits": "무궁무진한 가능성을 품었으며 온순하고 자유로운 감각을 지님",
        "reason": "틀에 매이지 않고 자유로우며 따뜻한 감성을 지닌 ISFP에게 이브이의 무한한 가능성은 호기심을 극대화합니다.\n서로의 고유한 결을 존중해주는 사랑스러운 조화입니다."
    },
    "INFP": {
        "mbti_desc": "열정적인 중재자",
        "name_kr": "님피아",
        "name_en": "Sylveon",
        "type": "✨ 페어리 타입",
        "img_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/700.png",
        "traits": "리본 모양 안테나로 다정한 감정을 전하는 친밀함의 아이콘",
        "reason": "풍부한 감수성과 낭만을 품은 INFP의 마음을 님피아의 따스하고 상스런 애정이 감싸 안아 줍니다.\n상처받기 쉬운 마음을 서로 보호해 주는 동화 같은 파트너십입니다."
    },
    "INTP": {
        "mbti_desc": "아이디어 파수꾼",
        "name_kr": "고라파덕",
        "name_en": "Psyduck",
        "type": "💧 물 타입",
        "img_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/54.png",
        "traits": "항상 생각에 잠겨있다가 결정적인 순간 폭발적인 천재적 염동력을 발휘",
        "reason": "머릿속이 기발한 생각으로 가득 찬 INTP와 멍해 보이지만 상상을 초월하는 능력을 발휘하는 고라파덕은 서로를 잘 이해합니다.\n엉뚱하면서도 독창적인 최고의 사색 친구입니다."
    },
    "ESTP": {
        "mbti_desc": "수완좋은 활동가",
        "name_kr": "피카츄",
        "name_en": "Pikachu",
        "type": "⚡ 전기 타입",
        "img_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png",
        "traits": "에너지 넘치고 즉흥적이며 어디서나 스파크 같은 활력을 발산함",
        "reason": "스릴과 도전을 즐기는 행동파 ESTP에게 피카츄의 통통 튀는 재기발랄함은 지루할 틈을 주지 않습니다.\n언제나 새로운 모험을 떠나게 만드는 최고의 활력소입니다."
    },
    "ESFP": {
        "mbti_desc": "자유로운 영혼의 연예인",
        "name_kr": "푸린",
        "name_en": "Jigglypuff",
        "type": "⚪ 노말 / ✨ 페어리",
        "img_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/39.png",
        "traits": "주목받는 것을 좋아하며 러블리하고 통통 튀는 무대의 주인공",
        "reason": "어디서나 분위기 메이커 역할을 담당하는 ESFP와 스타성이 풍부한 푸린은 완벽한 시너지입니다.\n삶을 하나의 즐거운 축제로 만드는 매력 넘치는 유쾌한 듀오입니다."
    },
    "ENFP": {
        "mbti_desc": "재기발랄한 활동가",
        "name_kr": "파이리",
        "name_en": "Charmander",
        "type": "🔥 불꽃 타입",
        "img_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/4.png",
        "traits": "꼬리 끝에 따스한 열정의 불꽃을 밝히며 호기심 많고 도전적인 성격",
        "reason": "아이디어가 끊임없이 샘솟고 열정이 넘치는 ENFP의 도전에 파이리의 불꽃 같은 순수한 열정이 큰 힘이 됩니다.\n함께 꿈을 향해 달리는 끝없는 원동력입니다."
    },
    "ENTP": {
        "mbti_desc": "뜨거운 논쟁을 즐기는 변론가",
        "name_kr": "팬텀",
        "name_en": "Gengar",
        "type": "👻 고스트 / ☠️ 독",
        "img_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/94.png",
        "traits": "재치와 기습적인 장난, 고정관념을 뒤흔드는 독창적인 매력",
        "reason": "기발한 발상과 유쾌한 티키타카를 즐기는 ENTP에게 팬텀의 엉뚱하고 재치 있는 유머 감각은 최고의 선물입니다.\n지루함을 싹 날려버릴 재치 만점 소울메이트입니다."
    },
    "ESTJ": {
        "mbti_desc": "엄격한 관리자",
        "name_kr": "윈디",
        "name_en": "Arcanine",
        "type": "🔥 불꽃 타입",
        "img_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/59.png",
        "traits": "위엄 있고 충성스러우며 강력한 리더십과 강직함을 겸비",
        "reason": "체계적이고 리더십이 뛰어난 ESTJ와 충직하고 위풍당당한 윈디는 단단한 질서와 상호 존중으로 연결됩니다.\n서로의 원칙을 확고히 지켜주는 든든하고 명예로운 파트너입니다."
    },
    "ESFJ": {
        "mbti_desc": "사교적인 외교관",
        "name_kr": "라이츄",
        "name_en": "Raichu",
        "type": "⚡ 전기 타입",
        "img_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/26.png",
        "traits": "상대방을 친근하게 다독여주며 밝고 든든하게 주위를 보살핌",
        "reason": "타인을 진심으로 아끼고 챙기는 따뜻한 ESFJ에게 라이츄의 통통 튀는 기분 좋은 에너지가 큰 위안을 줍니다.\n누구와도 잘 어울리는 최고 수준의 인싸 콤비입니다."
    },
    "ENFJ": {
        "mbti_desc": "정의로운 사회운동가",
        "name_kr": "망나뇽",
        "name_en": "Dragonite",
        "type": "🐉 드래곤 / 🕊️ 비행",
        "img_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/149.png",
        "traits": "상심한 사람이나 바다의 조난자를 돕는 온화하고 강인한 마음",
        "reason": "타인을 이끌고 선한 영향을 나누는 ENFJ와 넓은 품으로 모두를 품어주는 망나뇽은 세상을 더 따뜻하게 만드는 동반자입니다.\n따스함과 강함이 공존하는 아름다운 조합입니다."
    },
    "ENTJ": {
        "mbti_desc": "대담한 통솔자",
        "name_kr": "리자몽",
        "name_en": "Charizard",
        "type": "🔥 불꽃 / 🕊️ 비행",
        "img_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/6.png",
        "traits": "불타는 승부욕과 용맹함, 정상을 향해 거침없이 오르는 야망",
        "reason": "목표를 향해 확고한 비전으로 나아가는 ENTJ의 패기와 리자몽의 화끈한 에너지 및 실행력이 결합해 어떤 목표든 단숨에 정복해냅니다."
    }
}

# ==========================================
# 3. 메인 화면 레이아웃
# ==========================================
st.markdown("""
    <div class="title-header">
        <div class="main-title">💛 MBTI 단짝 포켓몬 찾기 💛</div>
        <div class="sub-title">당신의 성격과 꼭 닮은 운명의 단짝 포켓몬을 만나보세요!</div>
    </div>
""", unsafe_allow_html=True)

# MBTI 선택 상자
mbti_list = list(POKEMON_MBTI_DATA.keys())
selected_mbti = st.selectbox(
    "👉 당신의 MBTI 유형을 선택해 주세요",
    mbti_list,
    index=0
)

st.write("") # 간격 조절

# 단짝 찾기 버튼
if st.button("✨ 내 단짝 포켓몬 확인하기 ✨"):
    # 축하 화면 효과 (풍선 날리기)
    st.balloons()
    
    data = POKEMON_MBTI_DATA[selected_mbti]
    
    # 결과 출력
    st.markdown(f"""
        <div class="result-card">
            <p style="color: #B45309; font-size: 1.2rem; font-weight: 700; margin-bottom: 5px;">
                [{selected_mbti}] {data['mbti_desc']}
            </p>
            <div class="pokemon-name">{data['name_kr']}</div>
            <div class="pokemon-english">({data['name_en']})</div>
            <div class="type-badge">{data['type']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 이미지 중앙 정렬 표시
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(data["img_url"], use_container_width=True)
    
    # 상세 특징 및 어울리는 이유
    st.markdown(f"""
        <div class="info-box">
            <div class="info-title">⭐ {data['name_kr']}의 특징</div>
            <div>{data['traits']}</div>
        </div>
        <div class="info-box">
            <div class="info-title">🤝 단짝인 이유</div>
            <div>{data['reason'].replace('\n', '<br>')}</div>
        </div>
    """, unsafe_allow_html=True)

else:
    # 기본 안내 문구
    st.info("💡 위의 목록에서 MBTI를 고른 후 **[내 단짝 포켓몬 확인하기]** 버튼을 눌러주세요!")ㅡ먀ㅜ.ㅔㅛ
