import streamlit as st
import requests
import json
import datetime
import uuid
import os
from typing import Dict, Any, List

# API 엔드포인트 설정
# 환경 변수 또는 기본값 사용
API_URL = os.environ.get("API_URL", "http://localhost:8000")

# 페이지 설정
st.set_page_config(
    page_title="이메일 관리 어시스턴트",
    page_icon="📧",
    layout="wide",
)

# 세션 상태 초기화
if 'emails' not in st.session_state:
    # 샘플 이메일 추가
    st.session_state.emails = [
        {
            "id": str(uuid.uuid4()),
            "sender": "김영수",
            "sender_email": "kim.youngsoo@company.com",
            "subject": "프로젝트 진행 상황 보고서 요청",
            "date": "2025-04-04",
            "content": "안녕하세요,\n\n4월 10일까지 프로젝트 진행 상황 보고서를 제출해 주시기 바랍니다. 특히 일정 지연 사항과 해결 방안에 대해 상세히 기술해 주세요.\n\n감사합니다.\n김영수 드림",
            "read": False,
            "important": True
        },
        {
            "id": str(uuid.uuid4()),
            "sender": "이지원",
            "sender_email": "lee.jiwon@company.com",
            "subject": "분기별 성과 평가 일정 안내",
            "date": "2025-04-03",
            "content": "안녕하세요,\n\n분기별 성과 평가가 4월 15일부터 20일까지 진행될 예정입니다. 필요한 문서를 준비해 주시고, 일정을 확인하여 참석해 주시기 바랍니다.\n\n감사합니다.\n인사팀 이지원 드림",
            "read": False,
            "important": False
        },
    ]

if 'selected_email' not in st.session_state:
    st.session_state.selected_email = None

if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}

# API 호출 함수
def analyze_email(email: Dict[str, Any]) -> Dict[str, Any]:
    """이메일 분석 API 호출"""
    try:
        response = requests.post(
            f"{API_URL}/api/analyze_email",
            json={"email": email},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API 오류: {response.status_code} - {response.text}")
            return {
                "importance": "오류",
                "needs_response": "오류",
                "summary": "API 호출 중 오류가 발생했습니다.",
                "suggested_action": None
            }
    except Exception as e:
        st.error(f"API 호출 오류: {str(e)}")
        return {
            "importance": "오류",
            "needs_response": "오류",
            "summary": f"API 호출 중 오류가 발생했습니다: {str(e)}",
            "suggested_action": None
        }

def process_command(command: str, emails: List[Dict[str, Any]]) -> Dict[str, Any]:
    """명령 처리 API 호출"""
    try:
        response = requests.post(
            f"{API_URL}/api/process_command",
            json={"command": command, "emails": emails},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API 오류: {response.status_code} - {response.text}")
            return {
                "message": "API 호출 중 오류가 발생했습니다.",
                "filtered_emails": []
            }
    except Exception as e:
        st.error(f"API 호출 오류: {str(e)}")
        return {
            "message": f"API 호출 중 오류가 발생했습니다: {str(e)}",
            "filtered_emails": []
        }

def check_api_health() -> Dict[str, Any]:
    """API 상태 확인"""
    try:
        response = requests.get(f"{API_URL}/api/health", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "status": "error",
                "message": f"API 서버 오류: {response.status_code}",
                "llm_info": None
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"API 서버 연결 실패: {str(e)}",
            "llm_info": None
        }

# 앱 제목
st.title("📧 이메일 관리 어시스턴트")
st.markdown("LLM 기반 이메일 관리 도우미 - MVP 프로토타입")
st.markdown("---")

# 메인 레이아웃
col1, col2 = st.columns([4, 6])

# 좌측 컬럼: 이메일 목록 + 새 이메일 추가
with col1:
    # 새 이메일 추가 폼
    with st.expander("✉️ 새 이메일 추가", expanded=False):
        email_col1, email_col2 = st.columns(2)
        with email_col1:
            sender = st.text_input("보낸 사람:", key="new_sender")
            sender_email = st.text_input("보낸 사람 이메일:", key="new_sender_email")
        with email_col2:
            subject = st.text_input("제목:", key="new_subject")
            date = st.date_input("날짜:", datetime.datetime.now(), key="new_date")
        
        content = st.text_area("이메일 내용:", height=150, key="new_content")
        important = st.checkbox("중요 이메일로 표시", key="new_important")
        
        if st.button("이메일 추가", use_container_width=True):
            if sender and subject and content:
                new_email = {
                    "id": str(uuid.uuid4()),
                    "sender": sender,
                    "sender_email": sender_email,
                    "subject": subject,
                    "date": date.strftime("%Y-%m-%d"),
                    "content": content,
                    "read": False,
                    "important": important
                }
                st.session_state.emails.insert(0, new_email)
                st.success("이메일이 추가되었습니다!")
                st.rerun()
            else:
                st.error("보낸 사람, 제목, 내용은 필수 입력 항목입니다.")
    
    # 이메일 목록
    st.subheader("📥 이메일 목록")
    
    # 이메일 필터링을 위한 명령 입력
    command = st.text_input("명령을 입력하세요 (예: '중요한 이메일만 보여줘', '김영수가 보낸 이메일 찾아줘')")
    if command:
        if st.button("명령 실행", use_container_width=True):
            with st.spinner("명령 처리 중..."):
                response = process_command(command, st.session_state.emails)
                
                st.info(response['message'])
                
                if response.get('filtered_emails') and len(response['filtered_emails']) > 0:
                    display_emails = response['filtered_emails']
                else:
                    display_emails = st.session_state.emails
    else:
        display_emails = st.session_state.emails
    
    # 이메일 목록 표시
    if not display_emails:
        st.info("표시할 이메일이 없습니다.")
    else:
        for i, email in enumerate(display_emails):
            # 이메일 카드 스타일
            card_style = "background-color: #E3F2FD; border-radius: 5px; padding: 10px; margin: 5px 0; border-left: 4px solid "
            if email.get('important', False):
                card_style += "#F44336"  # 중요 이메일
            elif not email.get('read', False):
                card_style += "#2196F3"  # 읽지 않은 이메일
            else:
                card_style += "#BBDEFB"  # 일반 이메일
            
            with st.container():
                st.markdown(f"""
                <div style="{card_style}">
                    <strong>{email['sender']}</strong> ({email['date']})
                    <br>{'🔴 ' if email.get('important', False) else ''}{email['subject']}
                </div>
                """, unsafe_allow_html=True)
                
                col1_btn, col2_btn = st.columns([3, 1])
                with col1_btn:
                    if st.button("상세 보기", key=f"view_{i}", use_container_width=True):
                        st.session_state.selected_email = email['id']
                        # 읽음 표시
                        for e in st.session_state.emails:
                            if e['id'] == email['id']:
                                e['read'] = True
                        st.rerun()
                with col2_btn:
                    btn_label = "⭐해제" if email.get('important', False) else "⭐중요"
                    if st.button(btn_label, key=f"star_{i}", use_container_width=True):
                        for e in st.session_state.emails:
                            if e['id'] == email['id']:
                                e['important'] = not e.get('important', False)
                        st.rerun()

# 우측 컬럼: 이메일 상세 보기 + AI 분석
with col2:
    if st.session_state.selected_email:
        selected = next((e for e in st.session_state.emails if e['id'] == st.session_state.selected_email), None)
        
        if selected:
            st.subheader("📝 이메일 상세")
            
            # 이메일 헤더 정보
            st.markdown(f"""
            **제목**: {selected['subject']}  
            **보낸 사람**: {selected['sender']} ({selected['sender_email']})  
            **날짜**: {selected['date']}
            """)
            
            # 이메일 내용
            st.markdown("**내용**:")
            st.text_area("", selected['content'], height=200, disabled=True, label_visibility="collapsed")
            
            # AI 분석 버튼
            if st.button("AI 분석 요청", use_container_width=True):
                with st.spinner("이메일 분석 중..."):
                    analysis = analyze_email(selected)
                    st.session_state.analysis_results[selected['id']] = analysis
            
            # 분석 결과 표시
            if selected['id'] in st.session_state.analysis_results:
                analysis = st.session_state.analysis_results[selected['id']]
                
                st.subheader("🔍 AI 분석 결과")
                
                # 분석 결과 카드
                col_imp, col_resp = st.columns(2)
                with col_imp:
                    importance_color = {
                        "상": "#F44336",  # 빨강
                        "중": "#FB8C00",  # 주황
                        "하": "#4CAF50"   # 초록
                    }.get(analysis['importance'], "#9E9E9E")
                    
                    st.markdown(f"""
                    <div style="background-color: {importance_color}20; border-radius: 5px; padding: 10px; text-align: center;">
                        <span style="color: {importance_color}; font-weight: bold; font-size: 1.2em;">중요도: {analysis['importance']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_resp:
                    response_color = {
                        "필요": "#F44336",  # 빨강
                        "선택적": "#FB8C00",  # 주황
                        "불필요": "#4CAF50"  # 초록
                    }.get(analysis['needs_response'], "#9E9E9E")
                    
                    st.markdown(f"""
                    <div style="background-color: {response_color}20; border-radius: 5px; padding: 10px; text-align: center;">
                        <span style="color: {response_color}; font-weight: bold; font-size: 1.2em;">응답 필요성: {analysis['needs_response']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 요약
                st.markdown("**요약:**")
                st.info(analysis['summary'])
                
                # 제안된 조치 (있는 경우)
                if analysis.get('suggested_action'):
                    st.markdown("**제안된 조치:**")
                    st.success(analysis['suggested_action'])
    else:
        st.info("왼쪽에서 이메일을 선택하여 상세 내용을 확인하세요.")

# 푸터
st.markdown("---")
st.caption("이메일 관리 에이전트 프로토타입 v0.1 | 무료 오픈소스 LLM 기반")

# API 서버 연결 상태 표시
api_health = check_api_health()
if api_health['status'] == 'ok':
    llm_info = api_health.get('llm_info', {})
    llm_status = "🤖 실제 LLM" if not llm_info.get('is_dummy', True) else "⚠️ 더미 LLM (Ollama 없음)"
    st.sidebar.success(f"✅ API 서버 연결됨 | {llm_status}")
    st.sidebar.info(f"모델: {llm_info.get('model_name', '정보 없음')}")
else:
    st.sidebar.error(f"❌ {api_health['message']}")
    st.sidebar.warning("백엔드 서버를 먼저 실행해주세요")
