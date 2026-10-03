import streamlit as st
import math

# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm_PHẠM HOÀNG KIỀU TRANG",
    page_icon="💰",
    layout="centered"
)

# ==============================
# CSS GIAO DIỆN
# ==============================
st.markdown("""
<style>
    .main {
        background-color: #f5f7fa;
    }

    .title {
        text-align: center;
        color: #1565C0;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        color: #666666;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .result-box {
        padding: 20px;
        border-radius: 12px;
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        margin-top: 15px;
    }

    .result-title {
        font-size: 18px;
        font-weight: bold;
        color: #333333;
    }

    .result-value {
        font-size: 24px;
        font-weight: bold;
        color: #1565C0;
    }

    .total-box {
        padding: 20px;
        border-radius: 12px;
        background-color: #E3F2FD;
        border: 2px solid #1565C0;
        margin-top: 20px;
        text-align: center;
    }

    .total-title {
        font-size: 20px;
        font-weight: bold;
        color: #0D47A1;
    }

    .total-value {
        font-size: 30px;
        font-weight: bold;
        color: #0D47A1;
    }
</style>
""", unsafe_allow_html=True)


# ==============================
# HÀM ĐỊNH DẠNG TIỀN
# ==============================
def format_vnd(amount):
    return f"{amount:,.0f} VNĐ".replace(",", ".")


# ==============================
# TIÊU ĐỀ
# ==============================
st.markdown(
    '<div class="title">💰 TÍNH LÃI GỬI TIẾT KIỆM</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Công cụ tính tiền lãi tiền gửi tiết kiệm</div>',
    unsafe_allow_html=True
)


# ==============================
# NHẬP THÔNG TIN
# ==============================
st.subheader("📋 Thông tin tiền gửi")

col1, col2 = st.columns(2)

with col1:
    so_tien_gui = st.number_input(
        "💵 Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

with col2:
    lai_suat = st.number_input(
        "📈 Lãi suất (%/năm)",
        min_value=0.0,
        value=5.0,
        step=0.1,
        format="%.2f"
    )

col3, col4 = st.columns(2)

with col3:
    ky_han = st.number_input(
        "📅 Kỳ hạn (tháng)",
        min_value=1,
        max_value=120,
        value=12,
        step=1
    )

with col4:
    hinh_thuc = st.selectbox(
        "💳 Hình thức nhận lãi",
        [
            "Cuối kỳ",
            "Hàng tháng",
            "Hàng quý"
        ]
    )


# ==============================
# NÚT TÍNH TOÁN
# ==============================
st.markdown("---")

tinh_lai = st.button(
    "🧮 TÍNH LÃI",
    use_container_width=True,
    type="primary"
)


# ==============================
# TÍNH TOÁN
# ==============================
if tinh_lai:

    if so_tien_gui <= 0:
        st.error("⚠️ Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("⚠️ Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Chuyển lãi suất % sang số thập phân
    lai_suat_nam = lai_suat / 100

    # Số năm gửi
    so_nam = ky_han / 12

    # Tổng tiền lãi theo lãi đơn
    tong_tien_lai = so_tien_gui * lai_suat_nam * so_nam

    # ==============================
    # TÍNH THEO HÌNH THỨC NHẬN LÃI
    # ==============================

    if hinh_thuc == "Cuối kỳ":

        # Toàn bộ tiền lãi nhận một lần khi đáo hạn
        tien_lai_dinh_ky = tong_tien_lai
        so_ky_nhan_lai = 1
        ten_ky = "cuối kỳ"

    elif hinh_thuc == "Hàng tháng":

        # Lãi mỗi tháng
        tien_lai_dinh_ky = (
            so_tien_gui * lai_suat_nam / 12
        )

        so_ky_nhan_lai = ky_han
        ten_ky = "tháng"

    else:  # Hàng quý

        # Lãi mỗi quý
        tien_lai_dinh_ky = (
            so_tien_gui * lai_suat_nam / 4
        )

        so_ky_nhan_lai = math.ceil(ky_han / 3)
        ten_ky = "quý"

    # Tổng số tiền cuối cùng
    tong_tien = so_tien_gui + tong_tien_lai


    # ==============================
    # HIỂN THỊ KẾT QUẢ
    # ==============================

    st.success("✅ Tính toán thành công!")

    st.subheader("📊 Kết quả")

    # Tiền lãi định kỳ
    st.markdown(
        f"""
        <div class="result-box">
            <div class="result-title">
                💵 Tiền lãi {ten_ky}
            </div>
            <div class="result-value">
                {format_vnd(tien_lai_dinh_ky)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Tổng tiền lãi
    st.markdown(
        f"""
        <div class="result-box">
            <div class="result-title">
                📈 Tổng tiền lãi
            </div>
            <div class="result-value">
                {format_vnd(tong_tien_lai)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Tổng tiền gốc + lãi
    st.markdown(
        f"""
        <div class="total-box">
            <div class="total-title">
                💰 TỔNG TIỀN GỐC + LÃI
            </div>
            <div class="total-value">
                {format_vnd(tong_tien)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    # ==============================
    # CHI TIẾT KHOẢN GỬI
    # ==============================

    st.markdown("---")
    st.subheader("📝 Chi tiết khoản gửi")

    detail_col1, detail_col2 = st.columns(2)

    with detail_col1:
        st.write(f"**Số tiền gốc:** {format_vnd(so_tien_gui)}")
        st.write(f"**Kỳ hạn:** {ky_han} tháng")

    with detail_col2:
        st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
        st.write(f"**Nhận lãi:** {hinh_thuc}")

    # ==============================
    # BẢNG TÓM TẮT
    # ==============================

    st.markdown("---")
    st.subheader("📋 Bảng tổng hợp")

    data = {
        "Nội dung": [
            "Số tiền gửi",
            "Kỳ hạn",
            "Lãi suất",
            "Hình thức nhận lãi",
            "Tiền lãi định kỳ",
            "Tổng tiền lãi",
            "Tổng tiền gốc + lãi"
        ],
        "Kết quả": [
            format_vnd(so_tien_gui),
            f"{ky_han} tháng",
            f"{lai_suat:.2f}%/năm",
            hinh_thuc,
            format_vnd(tien_lai_dinh_ky),
            format_vnd(tong_tien_lai),
            format_vnd(tong_tien)
        ]
    }

    st.table(data)
