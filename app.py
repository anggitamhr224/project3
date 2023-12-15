import streamlit as st
from sqlalchemy import text

list_symptom = ['', 'Pria', 'Wanita']
list_posisi = ['','Penyerang', 'Gelandang', 'Bertahan', 'Kiper']

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://anggraeniervana:yMcg1tW6CRaL@ep-late-field-02299309.us-east-2.aws.neon.tech/web")
with conn.session as session:
    query = text('CREATE TABLE IF NOT EXISTS BIODATA (id serial, nama_pemain varchar, nama_pelatih varchar, jenis_kelamin char(25), \
                                                       posisi text, asal_club varchar, asal_negara varchar, tempat_lahir varchar, tanggal_lahir date, tinggi_badan varchar);')
    session.execute(query)

st.header('BIODATA PEMAIN BOLA TERBAIK')
page = st.sidebar.selectbox("Pilih Menu", ["View Data","Edit Data"])

if page == "View Data":
  
    search_input = st.text_input("Cari Nama Pemain Bola", "")

    query_str = f"SELECT * FROM BIODATA WHERE LOWER(nama_pemain) LIKE LOWER('%{search_input}%') OR LOWER(nama_pelatih) LIKE LOWER('%{search_input}%') OR LOWER(asal_club) LIKE LOWER('%{search_input}%') ORDER By id;"
    data = conn.query(query_str, ttl="0").set_index('id')
    st.dataframe(data)


if page == "Edit Data":
    if st.button('Tambah Data'):
        with conn.session as session:
            query = text('INSERT INTO biodata (nama_pemain, nama_pelatih, jenis_kelamin, \
                                                       posisi, asal_club, asal_negara, tempat_lahir, tanggal_lahir, tinggi_badan) \
                          VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9);')
            session.execute(query, {'1':'', '2':'', '3':'', '4':'[]', '5':'', '6':'', '7':'', '8':None, '9':''})
            session.commit()

    data = conn.query('SELECT * FROM biodata ORDER By id;', ttl="0")
    for _, result in data.iterrows():        
        id = result['id']
        nama_pemain_lama = result["nama_pemain"]
        nama_pelatih_lama = result["nama_pelatih"]
        jenis_kelamin_lama = result["jenis_kelamin"]
        posisi_lama = result["posisi"]
        asal_club_lama = result["asal_club"]
        asal_negara_lama = result["asal_negara"]
        tempat_lahir_lama = result["tempat_lahir"]
        tanggal_lahir_lama = result["tanggal_lahir"]
        tinggi_badan_lama = result["tinggi_badan"]

        with st.expander(f'a.n. {nama_pemain_lama}'):
            with st.form(f'data-{id}'):
                nama_pemain_baru = st.text_input("nama_pemain", nama_pemain_lama)
                nama_pelatih_baru = st.text_input("nama_pelatih", nama_pelatih_lama)
                jenis_kelamin_baru = st.selectbox("jenis_kelamin", list_symptom, list_symptom.index(jenis_kelamin_lama))
                posisi_baru = st.multiselect("posisi", ['Penyerang', 'Gelandang', 'Bertahan', 'Kiper'], eval(posisi_lama))
                asal_club_baru = st.text_input("asal_club", asal_club_lama)
                asal_negara_baru = st.text_input("asal_negara", asal_negara_lama)
                tempat_lahir_baru = st.text_input("tempat_lahir", tempat_lahir_lama)
                tanggal_lahir_baru = st.date_input("tanggal_lahir", tanggal_lahir_lama)
                tinggi_badan_baru = st.text_input("tinggi_badan", tinggi_badan_lama)
                
                col1, col2 = st.columns([1, 6])

                with col1:
                    if st.form_submit_button('UPDATE'):
                        with conn.session as session:
                            query = text('UPDATE biodata \
                                          SET nama_pemain=:1, nama_pelatih=:2, jenis_kelamin=:3, posisi=:4, \
                                          asal_club=:5, asal_negara=:6, tempat_lahir=:7, tanggal_lahir=:8, tinggi_badan=:9 \
                                          WHERE id=:10;')
                            session.execute(query, {'1':nama_pemain_baru, '2':nama_pelatih_baru, '3':jenis_kelamin_baru, '4':str(posisi_baru), 
                                                    '5':asal_club_baru, '6':asal_negara_baru, '7':tempat_lahir_baru, '8':tanggal_lahir_baru, '9':tinggi_badan_baru, '10':id})
                            session.commit()
                            st.experimental_rerun()
                
                with col2:
                    if st.form_submit_button('DELETE'):
                        query = text(f'DELETE FROM biodata WHERE id=:1;')
                        session.execute(query, {'1':id})
                        session.commit()
                        st.experimental_rerun()
