CREATE VIEW audit.v_son_audit AS
 SELECT id,
    cedvel_adi,
    emeliyyat,
    setir_id,
    istifadeci,
    vaxt
   FROM audit.audit_log
  ORDER BY vaxt DESC
 LIMIT 50;
CREATE VIEW elm.v_doktorant_sayi AS
 SELECT p.id AS proqram_id,
    p.ad AS proqram,
    (count(d.id))::integer AS doktorant_sayi
   FROM (elm.doktorantura_proqramlari p
     LEFT JOIN elm.doktorantlar d ON ((d.proqram_id = p.id)))
  GROUP BY p.id, p.ad;
CREATE VIEW elm.v_tedqiqat_layiheleri AS
 SELECT l.id,
    l.ad,
    i.ad AS istiqamet,
    l.status,
    ((e.soyad || ' '::text) || e.ad) AS rehber,
    l.baslama_tarixi,
    l.bitme_tarixi
   FROM ((elm.tedqiqat_layiheleri l
     JOIN elm.tedqiqat_istiqametleri i ON ((i.id = l.istiqamet_id)))
     LEFT JOIN kadrlar.emekdaslar e ON ((e.id = l.rehber_id)));
CREATE VIEW kadrlar.v_emekdas_tam AS
 SELECT e.id,
    ((((e.soyad || ' '::text) || e.ad) || ' '::text) || e.ata_adi) AS tam_adi,
    v.ad AS vezife,
    s.ad AS shobe,
    m.ad AS merkez,
    e.maas,
    st.ad AS status
   FROM ((((kadrlar.emekdaslar e
     LEFT JOIN struktur.vezifeler v ON ((v.id = e.vezife_id)))
     LEFT JOIN struktur.shobeler s ON ((s.id = e.shobe_id)))
     LEFT JOIN struktur.merkezler m ON ((m.id = e.merkez_id)))
     LEFT JOIN ortaq.is_statuslari st ON ((st.id = e.is_status_id)));
CREATE VIEW maliyye.v_budce_istifadesi AS
 SELECT id AS budce_id,
    il,
    menbe,
    mebleg AS plan_mebleg,
    COALESCE(( SELECT sum(x.mebleg) AS sum
           FROM maliyye.maliyye_emeliyyatlari x
          WHERE ((x.budce_id = b.id) AND (x.nov = 'xerc'::text))), (0)::numeric) AS xerclenmis,
    (mebleg - COALESCE(( SELECT sum(x.mebleg) AS sum
           FROM maliyye.maliyye_emeliyyatlari x
          WHERE ((x.budce_id = b.id) AND (x.nov = 'xerc'::text))), (0)::numeric)) AS qaliq
   FROM maliyye.budce b;
CREATE VIEW maliyye.v_satinalma_veziyyeti AS
 SELECT status,
    (count(*))::integer AS say,
    COALESCE(sum(mebleg), (0)::numeric) AS umumi_mebleg
   FROM maliyye.satinalmalar
  GROUP BY status;
CREATE VIEW struktur.v_merkez_shobe_sayi AS
 SELECT m.id AS merkez_id,
    m.ad AS merkez,
    (count(s.id))::integer AS shobe_sayi
   FROM (struktur.merkezler m
     LEFT JOIN struktur.shobeler s ON ((s.merkez_id = m.id)))
  GROUP BY m.id, m.ad;
CREATE VIEW tehsil.v_telim_qrup_istirakci_sayi AS
 SELECT q.id AS qrup_id,
    q.ad AS qrup,
    p.ad AS proqram,
    q.status,
    (count(i.id))::integer AS istirakci_sayi
   FROM ((tehsil.telim_qruplari q
     JOIN tehsil.telim_proqramlari p ON ((p.id = q.proqram_id)))
     LEFT JOIN tehsil.telim_istirakcilari i ON ((i.qrup_id = q.id)))
  GROUP BY q.id, q.ad, p.ad, q.status;
