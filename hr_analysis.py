import streamlit as st
import pandas as pd
import altair as alt

# 페이지 설정
st.set_page_config(page_title="HR Analytics Dashboard", page_icon="👥", layout="wide")

# 제목
st.title("👥 HR Analytics Dashboard")
st.markdown("### 퇴직율 분석 및 인사이트")

# 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_csv('HR Data.csv')
    # Yes/No를 1/0으로 변환
    df['퇴직여부_수치'] = (df['퇴직여부'] == 'Yes').astype(int)
    return df

try:
    df = load_data()
    
    # 기본 통계
    col1, col2, col3, col4 = st.columns(4)
    total_employees = len(df)
    left_employees = len(df[df['퇴직여부'] == 'Yes'])
    retention_rate = ((total_employees - left_employees) / total_employees) * 100
    
    col1.metric("전체 직원 수", f"{total_employees:,}명")
    col2.metric("퇴직자 수", f"{left_employees:,}명")
    col3.metric("유지율", f"{retention_rate:.1f}%")
    col4.metric("퇴직율", f"{100-retention_rate:.1f}%")
    
    # 부서별 퇴직율
    st.markdown("### 📊 부서별 퇴직율")
    dept_turnover = df.groupby('부서')['퇴직여부_수치'].mean() * 100
    dept_df = dept_turnover.reset_index()
    dept_df.columns = ['부서', '퇴직율']
    dept_df['퇴직율'] = dept_df['퇴직율'].round(1)
    
    dept_chart = alt.Chart(dept_df).mark_bar().encode(
        x='부서',
        y='퇴직율',
        text=alt.Text('퇴직율', format='.1f')
    ).properties(height=400)
    
    text = dept_chart.mark_text(
        align='center',
        baseline='bottom',
        dy=-5
    ).encode(text=alt.Text('퇴직율', format='.1f'))
    
    st.altair_chart(dept_chart + text, use_container_width=True)
    
    # 급여인상율과 퇴직율
    col5, col7 = st.columns(2)
    
    with col5:
        st.markdown("### 💰 급여인상율과 퇴직율")
        salary_increase_turnover = df.groupby('급여증가분백분율')['퇴직여부_수치'].mean() * 100
        salary_df = salary_increase_turnover.reset_index()
        salary_df.columns = ['급여인상율', '퇴직율']
        salary_df['퇴직율'] = salary_df['퇴직율'].round(1)
        
        salary_chart = alt.Chart(salary_df).mark_line(point=True).encode(
            x=alt.X('급여인상율', title='급여인상율 (%)'),
            y=alt.Y('퇴직율', title='퇴직율 (%)'),
            text=alt.Text('퇴직율', format='.1f')
        ).properties(height=400)
        
        text = salary_chart.mark_text(
            align='center',
            baseline='bottom',
            dy=-10
        ).encode(text=alt.Text('퇴직율', format='.1f'))
        
        st.altair_chart(salary_chart + text, use_container_width=True)
    
    with col7:
        st.markdown("### ⏰ 야근정도별 퇴직율")
        overtime = df.groupby('야근정도')['퇴직여부_수치'].mean() * 100
        overtime_df = overtime.reset_index()
        overtime_df.columns = ['야근정도', '퇴직율']
        overtime_df['퇴직율'] = overtime_df['퇴직율'].round(1)
        
        overtime_chart = alt.Chart(overtime_df).mark_bar().encode(
            x='야근정도',
            y='퇴직율',
            text=alt.Text('퇴직율', format='.1f')
        ).properties(height=400)
        
        text = overtime_chart.mark_text(
            align='center',
            baseline='bottom',
            dy=-5
        ).encode(text=alt.Text('퇴직율', format='.1f'))
        
        st.altair_chart(overtime_chart + text, use_container_width=True)
    
    # 주요 인사이트
    st.markdown("### 🔍 주요 인사이트")
    st.markdown("""
    1. **부서별 분석**: 퇴직율이 가장 높은 부서를 확인하고 해당 부서의 업무 환경 개선이 필요합니다.
    2. **급여인상**: 급여인상율과 퇴직율의 관계를 파악하여 적절한 보상 인상 정책을 검토합니다.
    3. **야근 영향**: 야근정도가 퇴직율에 미치는 영향을 분석하여 업무 강도 조절이 필요합니다.
    """)
    
except FileNotFoundError:
    st.error("'HR Data.csv' 파일을 찾을 수 없습니다. 파일이 올바른 위치에 있는지 확인해주세요.")
