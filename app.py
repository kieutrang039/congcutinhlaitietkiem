import streamlit as st
st.image("logo.jpg")
import math

# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm_PHẠM HOÀNG KIỀU TRANG",
    page_icon="💰",
    layout="centered"
)

# =========================================================
# HIỂN THỊ LOGO
# =========================================================

try:
    st.image("logo.jpg", use_container_width=True)
except:
    pass


# =========================================================
# CSS GIAO DIỆN
# =========================================================

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

.bank-box {
    padding: 15px;
    border-radius: 12px;
    background-color: #F1F8E9;
    border: 1px solid #8BC34A;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def format_vnd(amount):
    return f"{amount:,.0f} VNĐ".replace(",", ".")


# =========================================================
# DỮ LIỆU LÃI SUẤT THAM CHIẾU
# =========================================================
# Đơn vị: %/năm
#
# Lưu ý:
# Đây là dữ liệu tham chiếu để minh họa chức năng.
# Lãi suất thực tế cần kiểm tra lại với ngân hàng.
# =========================================================

LAI_SUAT_NGAN_HANG = {

    "Vietcombank": {
        1: 1.60,
        3: 1.90,
        6: 2.90,
        12: 4.60,
        24: 4.70
    },

    "BIDV": {
        1: 1.70,
        3: 2.00,
        6: 3.00,
        12: 4.70,
        24: 4.80
    },

    "VietinBank": {
        1: 1.70,
        3: 2.00,
        6: 3.00,
        12: 4.80,
        24: 4.80
    },

    "Agribank": {
        1: 1.60,
        3: 1.90,
        6: 2.90,
        12: 4.70,
        24: 4.80
    },

    "Techcombank": {
        1: 3.00,
        3: 3.20,
        6: 4.00,
        12: 4.90,
        24: 5.00
    },

    "MB Bank": {
        1: 2.40,
        3: 2.70,
        6: 3.50,
        12: 4.80,
        24: 5.00
    },

    "ACB": {
        1: 2.50,
        3: 2.80,
        6: 3.60,
        12: 4.70,
        24: 4.90
    }
}


# =========================================================
# HÀM TÌM LÃI SUẤT NGÂN HÀNG
# =========================================================

def lay_lai_suat(ngan_hang, ky_han):

    bang_lai_suat = LAI_SUAT_NGAN_HANG[ngan_hang]

    # Nếu có đúng kỳ hạn
    if ky_han in bang_lai_suat:
        return bang_lai_suat[ky_han]

    # Nếu không có đúng kỳ hạn,
    # tìm kỳ hạn gần nhất
    ky_han_gan_nhat = min(
        bang_lai_suat.keys(),
        key=lambda x: abs(x - ky_han)
    )

    return bang_lai_suat[ky_han_gan_nhat]


# =========================================================
# HÀM TÍNH LÃI ĐƠN
# =========================================================

def tinh_lai_don(
    tien_goc,
    lai_suat,
    ky_han_thang
):

    lai_suat_nam = lai_suat / 100

    so_nam = ky_han_thang / 12

    tien_lai = (
        tien_goc
        * lai_suat_nam
        * so_nam
    )

    tong_tien = tien_goc + tien_lai

    return tien_lai, tong_tien


# =========================================================
# HÀM TÍNH LÃI KÉP
# =========================================================

def tinh_lai_kep(
    tien_goc,
    lai_suat,
    ky_han_thang,
    hinh_thuc
):

    lai_suat_nam = lai_suat / 100

    so_nam = ky_han_thang / 12

    # Số lần nhập lãi trong 1 năm

    if hinh_thuc == "Hàng tháng":
        n = 12

    elif hinh_thuc == "Hàng quý":
        n = 4

    else:
        n = 1

    # Công thức lãi kép
    tong_tien = (
        tien_goc
        * (1 + lai_suat_nam / n)
        ** (n * so_nam)
    )

    tien_lai = tong_tien - tien_goc

    return tien_lai, tong_tien


# =========================================================
# HÀM TÍNH LÃI ĐỊNH KỲ
# =========================================================

def tinh_lai_dinh_ky(
    tien_goc,
    lai_suat,
    hinh_thuc,
    tong_tien_lai=None
):

    lai_suat_nam = lai_suat / 100

    if hinh_thuc == "Hàng tháng":

        return (
            tien_goc
            * lai_suat_nam
            / 12
        )

    elif hinh_thuc == "Hàng quý":

        return (
            tien_goc
            * lai_suat_nam
            / 4
        )

    else:

        if tong_tien_lai is not None:
            return tong_tien_lai

        return tien_goc * lai_suat_nam


# =========================================================
# TIÊU ĐỀ
# =========================================================

st.markdown(
    '<div class="title">'
    '💰 TÍNH LÃI GỬI TIẾT KIỆM_PHẠM HOÀNG KIỀU TRANG'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Công cụ tính tiền lãi tiền gửi tiết kiệm thông minh'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# CHỌN PHƯƠNG PHÁP TÍNH LÃI
# =========================================================

st.subheader("🧮 Phương pháp tính lãi")

phuong_phap = st.radio(
    "Chọn phương pháp:",
    [
        "Lãi đơn",
        "Lãi kép"
    ],
    horizontal=True
)


# =========================================================
# NHẬP THÔNG TIN TIỀN GỬI
# =========================================================

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

    ky_han = st.selectbox(
        "📅 Kỳ hạn (tháng)",
        [
            1,
            3,
            6,
            9,
            12,
            18,
            24,
            36,
            48,
            60
        ],
        index=4
    )


col3, col4 = st.columns(2)

with col3:

    hinh_thuc = st.selectbox(
        "💳 Hình thức nhận lãi",
        [
            "Cuối kỳ",
            "Hàng tháng",
            "Hàng quý"
        ]
    )


with col4:

    ngan_hang = st.selectbox(
        "🏦 Chọn ngân hàng",
        list(LAI_SUAT_NGAN_HANG.keys())
    )


# =========================================================
# THAM CHIẾU LÃI SUẤT
# =========================================================

st.markdown("---")

st.subheader("🏦 Tham chiếu lãi suất ngân hàng")

lai_suat_tham_chieu = lay_lai_suat(
    ngan_hang,
    ky_han
)

st.markdown(
    f"""
    <div class="bank-box">

        <b>🏦 Ngân hàng:</b> {ngan_hang}<br><br>

        <b>📅 Kỳ hạn:</b> {ky_han} tháng<br><br>

        <b>📈 Lãi suất tham chiếu:</b>
        <span style="font-size:22px;font-weight:bold;color:#2E7D32;">
            {lai_suat_tham_chieu:.2f}%/năm
        </span>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# CHỌN CÁCH NHẬP LÃI SUẤT
# =========================================================

su_dung_lai_suat_tham_chieu = st.checkbox(
    "🔄 Sử dụng lãi suất tham chiếu của ngân hàng",
    value=True
)


if su_dung_lai_suat_tham_chieu:

    lai_suat = lai_suat_tham_chieu

    st.info(
        f"Lãi suất {ngan_hang} được sử dụng: "
        f"**{lai_suat:.2f}%/năm**"
    )

else:

    lai_suat = st.number_input(
        "📈 Nhập lãi suất (%/năm)",
        min_value=0.0,
        value=float(lai_suat_tham_chieu),
        step=0.1,
        format="%.2f"
    )


# =========================================================
# NÚT TÍNH TOÁN
# =========================================================

st.markdown("---")

tinh_lai = st.button(
    "🧮 TÍNH LÃI",
    use_container_width=True,
    type="primary"
)


# =========================================================
# TÍNH TOÁN
# =========================================================

if tinh_lai:

    # Kiểm tra số tiền
    if so_tien_gui <= 0:

        st.error(
            "⚠️ Vui lòng nhập số tiền gửi lớn hơn 0."
        )

        st.stop()


    # Kiểm tra lãi suất
    if lai_suat < 0:

        st.error(
            "⚠️ Lãi suất không được nhỏ hơn 0."
        )

        st.stop()


    # =====================================================
    # LÃI ĐƠN
    # =====================================================

    lai_don, tong_don = tinh_lai_don(
        so_tien_gui,
        lai_suat,
        ky_han
    )


    # =====================================================
    # LÃI KÉP
    # =====================================================

    lai_kep, tong_kep = tinh_lai_kep(
        so_tien_gui,
        lai_suat,
        ky_han,
        hinh_thuc
    )


    # =====================================================
    # CHỌN KẾT QUẢ
    # =====================================================

    if phuong_phap == "Lãi đơn":

        tong_tien_lai = lai_don

        tong_tien = tong_don

    else:

        tong_tien_lai = lai_kep

        tong_tien = tong_kep


    # =====================================================
    # LÃI ĐỊNH KỲ
    # =====================================================

    if hinh_thuc == "Cuối kỳ":

        tien_lai_dinh_ky = tong_tien_lai
        ten_ky = "cuối kỳ"

    elif hinh_thuc == "Hàng tháng":

        if phuong_phap == "Lãi đơn":

            tien_lai_dinh_ky = (
                so_tien_gui
                * lai_suat / 100
                / 12
            )

        else:

            tien_lai_dinh_ky = (
                so_tien_gui
                * (
                    (1 + lai_suat / 100 / 12)
                    - 1
                )
            )

        ten_ky = "tháng"

    else:

        if phuong_phap == "Lãi đơn":

            tien_lai_dinh_ky = (
                so_tien_gui
                * lai_suat / 100
                / 4
            )

        else:

            tien_lai_dinh_ky = (
                so_tien_gui
                * (
                    (1 + lai_suat / 100 / 4)
                    - 1
                )
            )

        ten_ky = "quý"


    # =====================================================
    # HIỂN THỊ KẾT QUẢ
    # =====================================================

    st.success(
        f"✅ Tính toán thành công theo phương pháp **{phuong_phap}**!"
    )

    st.subheader("📊 Kết quả")


    # -----------------------------------------------------
    # 3 Ô KẾT QUẢ
    # -----------------------------------------------------

    result_col1, result_col2, result_col3 = st.columns(3)


    with result_col1:

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


    with result_col2:

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


    with result_col3:

        st.markdown(
            f"""
            <div class="result-box">

                <div class="result-title">
                    💰 Tổng gốc + lãi
                </div>

                <div class="result-value">
                    {format_vnd(tong_tien)}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # TỔNG TIỀN
    # =====================================================

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


    # =====================================================
    # CHI TIẾT KHOẢN GỬI
    # =====================================================

    st.markdown("---")

    st.subheader("📝 Chi tiết khoản gửi")

    detail_col1, detail_col2 = st.columns(2)


    with detail_col1:

        st.write(
            f"**Số tiền gốc:** "
            f"{format_vnd(so_tien_gui)}"
        )

        st.write(
            f"**Kỳ hạn:** "
            f"{ky_han} tháng"
        )

        st.write(
            f"**Ngân hàng:** "
            f"{ngan_hang}"
        )


    with detail_col2:

        st.write(
            f"**Lãi suất:** "
            f"{lai_suat:.2f}%/năm"
        )

        st.write(
            f"**Phương pháp:** "
            f"{phuong_phap}"
        )

        st.write(
            f"**Nhận lãi:** "
            f"{hinh_thuc}"
        )


    # =====================================================
    # SO SÁNH LÃI ĐƠN - LÃI KÉP
    # =====================================================

    st.markdown("---")

    st.subheader("⚖️ So sánh lãi đơn và lãi kép")


    bang_so_sanh = pd.DataFrame({

        "Phương pháp": [
            "Lãi đơn",
            "Lãi kép"
        ],

        "Tổng tiền lãi": [
            format_vnd(lai_don),
            format_vnd(lai_kep)
        ],

        "Tổng tiền gốc + lãi": [
            format_vnd(tong_don),
            format_vnd(tong_kep)
        ]
    })


    st.table(bang_so_sanh)


    # =====================================================
    # CHÊNH LỆCH
    # =====================================================

    chenh_lech = lai_kep - lai_don


    if chenh_lech > 0:

        st.info(
            f"💡 Với khoản tiền này, lãi kép tạo ra "
            f"nhiều hơn lãi đơn khoảng "
            f"**{format_vnd(chenh_lech)}** "
            f"trong cùng kỳ hạn."
        )

    elif chenh_lech == 0:

        st.info(
            "💡 Hai phương pháp cho kết quả bằng nhau."
        )

    else:

        st.info(
            f"💡 Chênh lệch tiền lãi: "
            f"{format_vnd(abs(chenh_lech))}"
        )


    # =====================================================
    # BIỂU ĐỒ
    # =====================================================

    st.markdown("---")

    st.subheader("📊 Biểu đồ so sánh")

    chart_data = pd.DataFrame({

        "Lãi đơn": [lai_don],

        "Lãi kép": [lai_kep]
    })

    st.bar_chart(chart_data)


    # =====================================================
    # BẢNG TỔNG HỢP
    # =====================================================

    st.markdown("---")

    st.subheader("📋 Bảng tổng hợp")


    data = {

        "Nội dung": [

            "Ngân hàng",

            "Số tiền gửi",

            "Kỳ hạn",

            "Lãi suất",

            "Phương pháp tính",

            "Hình thức nhận lãi",

            "Tiền lãi định kỳ",

            "Tổng tiền lãi",

            "Tổng tiền gốc + lãi"
        ],

        "Kết quả": [

            ngan_hang,

            format_vnd(so_tien_gui),

            f"{ky_han} tháng",

            f"{lai_suat:.2f}%/năm",

            phuong_phap,

            hinh_thuc,

            format_vnd(tien_lai_dinh_ky),

            format_vnd(tong_tien_lai),

            format_vnd(tong_tien)
        ]
    }


    st.table(data)


# =========================================================
# GHI CHÚ
# =========================================================

st.markdown("---")

st.warning(
    "⚠️ Lãi suất ngân hàng trong ứng dụng là dữ liệu tham chiếu "
    "để phục vụ tính toán. Lãi suất thực tế có thể thay đổi "
    "theo thời điểm, số tiền gửi, kỳ hạn và chính sách của từng ngân hàng."
)

st.caption(
    "💡 Ứng dụng được xây dựng bằng Streamlit | "
    "PHẠM HOÀNG KIỀU TRANG"
)
