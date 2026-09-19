--
-- PostgreSQL database dump
--

\restrict ZuCCv71ouSVfW6LkiQpwQVcvo5SKQ9OfgkcXtgRSQKNhQ9fvgsiX0I41vFkc7rq

-- Dumped from database version 18.6 (Homebrew)
-- Dumped by pg_dump version 18.6 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: ai; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA ai;


--
-- Name: audit; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA audit;


--
-- Name: elm; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA elm;


--
-- Name: kadrlar; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA kadrlar;


--
-- Name: logistika; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA logistika;


--
-- Name: maliyye; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA maliyye;


--
-- Name: metodika; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA metodika;


--
-- Name: ortaq; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA ortaq;


--
-- Name: qiymetlendirme; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA qiymetlendirme;


--
-- Name: sened; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA sened;


--
-- Name: struktur; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA struktur;


--
-- Name: tehsil; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA tehsil;


--
-- Name: fn_audit_yaz(); Type: FUNCTION; Schema: audit; Owner: -
--

CREATE FUNCTION audit.fn_audit_yaz() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_setir_id TEXT;
BEGIN
    IF TG_OP = 'DELETE' THEN
        v_setir_id := OLD.id::TEXT;
    ELSE
        v_setir_id := NEW.id::TEXT;
    END IF;
    INSERT INTO audit.audit_log (cedvel_adi, emeliyyat, setir_id, istifadeci, qeyd)
    VALUES (TG_TABLE_SCHEMA || '.' || TG_TABLE_NAME, TG_OP, v_setir_id,
            current_user, 'Trigger ilə avtomatik qeyd');
    RETURN NULL;
END;
$$;


--
-- Name: fn_doktorant_status_say(text); Type: FUNCTION; Schema: elm; Owner: -
--

CREATE FUNCTION elm.fn_doktorant_status_say(p_status text) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_say INT;
BEGIN
    SELECT count(*)::INT INTO v_say
    FROM elm.doktorantlar WHERE status = p_status;
    RETURN v_say;
END;
$$;


--
-- Name: fn_emekdas_tam_adi(bigint); Type: FUNCTION; Schema: kadrlar; Owner: -
--

CREATE FUNCTION kadrlar.fn_emekdas_tam_adi(p_id bigint) RETURNS text
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_tam_adi TEXT;
BEGIN
    SELECT soyad || ' ' || ad || ' ' || ata_adi
    INTO v_tam_adi
    FROM kadrlar.emekdaslar WHERE id = p_id;
    RETURN COALESCE(v_tam_adi, 'Tapılmadı');
END;
$$;


--
-- Name: fn_gun_sayi_hesabla(); Type: FUNCTION; Schema: kadrlar; Owner: -
--

CREATE FUNCTION kadrlar.fn_gun_sayi_hesabla() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NEW.baslama_tarixi IS NOT NULL AND NEW.bitme_tarixi IS NOT NULL THEN
        NEW.gun_sayi := (NEW.bitme_tarixi - NEW.baslama_tarixi) + 1;
    END IF;
    RETURN NEW;
END;
$$;


--
-- Name: fn_maas_fondu(); Type: FUNCTION; Schema: kadrlar; Owner: -
--

CREATE FUNCTION kadrlar.fn_maas_fondu() RETURNS numeric
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_cem NUMERIC;
BEGIN
    SELECT COALESCE(sum(maas), 0) INTO v_cem
    FROM kadrlar.emekdaslar WHERE aktiv = TRUE;
    RETURN v_cem;
END;
$$;


--
-- Name: fn_budce_il_cemi(integer); Type: FUNCTION; Schema: maliyye; Owner: -
--

CREATE FUNCTION maliyye.fn_budce_il_cemi(p_il integer) RETURNS numeric
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_cem NUMERIC;
BEGIN
    SELECT COALESCE(sum(mebleg), 0) INTO v_cem
    FROM maliyye.budce WHERE il = p_il;
    RETURN v_cem;
END;
$$;


--
-- Name: fn_budce_qaliq(integer); Type: FUNCTION; Schema: maliyye; Owner: -
--

CREATE FUNCTION maliyye.fn_budce_qaliq(p_budce_id integer) RETURNS numeric
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_plan NUMERIC;
    v_xerc NUMERIC;
BEGIN
    SELECT mebleg INTO v_plan FROM maliyye.budce WHERE id = p_budce_id;
    SELECT COALESCE(sum(mebleg), 0) INTO v_xerc
    FROM maliyye.maliyye_emeliyyatlari
    WHERE budce_id = p_budce_id AND nov = 'xerc';
    RETURN COALESCE(v_plan, 0) - v_xerc;
END;
$$;


--
-- Name: fn_shobe_sayi(integer); Type: FUNCTION; Schema: struktur; Owner: -
--

CREATE FUNCTION struktur.fn_shobe_sayi(p_merkez_id integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_say INT;
BEGIN
    SELECT count(*)::INT INTO v_say
    FROM struktur.shobeler WHERE merkez_id = p_merkez_id;
    RETURN v_say;
END;
$$;


--
-- Name: fn_sertifikasiya_ortalamasi(); Type: FUNCTION; Schema: tehsil; Owner: -
--

CREATE FUNCTION tehsil.fn_sertifikasiya_ortalamasi() RETURNS numeric
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_ort NUMERIC;
BEGIN
    SELECT COALESCE(round(avg(bal), 2), 0) INTO v_ort
    FROM tehsil.sertifikasiya WHERE netice = 'keçdi';
    RETURN v_ort;
END;
$$;


--
-- Name: fn_telim_istirakci_sayi(integer); Type: FUNCTION; Schema: tehsil; Owner: -
--

CREATE FUNCTION tehsil.fn_telim_istirakci_sayi(p_qrup_id integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_say INT;
BEGIN
    SELECT count(*)::INT INTO v_say
    FROM tehsil.telim_istirakcilari WHERE qrup_id = p_qrup_id;
    RETURN v_say;
END;
$$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: ai_promptlar; Type: TABLE; Schema: ai; Owner: -
--

CREATE TABLE ai.ai_promptlar (
    id integer NOT NULL,
    ad text NOT NULL,
    tip text DEFAULT 'sual-cavab'::text NOT NULL,
    prompt_metni text NOT NULL,
    aktiv boolean DEFAULT true NOT NULL
);


--
-- Name: TABLE ai_promptlar; Type: COMMENT; Schema: ai; Owner: -
--

COMMENT ON TABLE ai.ai_promptlar IS 'AI prompt şablonları';


--
-- Name: ai_promptlar_id_seq; Type: SEQUENCE; Schema: ai; Owner: -
--

ALTER TABLE ai.ai_promptlar ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME ai.ai_promptlar_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: ai_sorghular; Type: TABLE; Schema: ai; Owner: -
--

CREATE TABLE ai.ai_sorghular (
    id bigint NOT NULL,
    istifadeci text DEFAULT CURRENT_USER,
    sorghu text NOT NULL,
    cavab text,
    model text DEFAULT 'deepseek'::text,
    token_sayi integer DEFAULT 0,
    vaxt timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: TABLE ai_sorghular; Type: COMMENT; Schema: ai; Owner: -
--

COMMENT ON TABLE ai.ai_sorghular IS 'AI sorğu-cavab jurnalı (chat)';


--
-- Name: ai_sorghular_id_seq; Type: SEQUENCE; Schema: ai; Owner: -
--

ALTER TABLE ai.ai_sorghular ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME ai.ai_sorghular_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: embeddingler; Type: TABLE; Schema: ai; Owner: -
--

CREATE TABLE ai.embeddingler (
    id bigint NOT NULL,
    cedvel_adi text NOT NULL,
    sened_id integer,
    metn text,
    vektor jsonb,
    yaradilma timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: TABLE embeddingler; Type: COMMENT; Schema: ai; Owner: -
--

COMMENT ON TABLE ai.embeddingler IS 'Sənədlərin vektor embedding-ləri (RAG üçün)';


--
-- Name: embeddingler_id_seq; Type: SEQUENCE; Schema: ai; Owner: -
--

ALTER TABLE ai.embeddingler ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME ai.embeddingler_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: audit_log; Type: TABLE; Schema: audit; Owner: -
--

CREATE TABLE audit.audit_log (
    id bigint NOT NULL,
    cedvel_adi text NOT NULL,
    emeliyyat text NOT NULL,
    setir_id text,
    istifadeci text DEFAULT CURRENT_USER,
    vaxt timestamp with time zone DEFAULT now() NOT NULL,
    qeyd text
);


--
-- Name: TABLE audit_log; Type: COMMENT; Schema: audit; Owner: -
--

COMMENT ON TABLE audit.audit_log IS 'Bütün dəyişikliklərin audit jurnalı';


--
-- Name: audit_log_id_seq; Type: SEQUENCE; Schema: audit; Owner: -
--

ALTER TABLE audit.audit_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME audit.audit_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: v_son_audit; Type: VIEW; Schema: audit; Owner: -
--

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


--
-- Name: doktorantlar; Type: TABLE; Schema: elm; Owner: -
--

CREATE TABLE elm.doktorantlar (
    id integer NOT NULL,
    proqram_id integer NOT NULL,
    ad text NOT NULL,
    soyad text NOT NULL,
    ata_adi text NOT NULL,
    status text DEFAULT 'tehsil alir'::text NOT NULL,
    qebul_tarixi date,
    rehber_id bigint,
    mudafie_tarixi date,
    qeyd text
);


--
-- Name: TABLE doktorantlar; Type: COMMENT; Schema: elm; Owner: -
--

COMMENT ON TABLE elm.doktorantlar IS 'Doktorantlar (fəlsəfə doktoru və elmlər doktoru)';


--
-- Name: doktorantlar_id_seq; Type: SEQUENCE; Schema: elm; Owner: -
--

ALTER TABLE elm.doktorantlar ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME elm.doktorantlar_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: doktorantura_proqramlari; Type: TABLE; Schema: elm; Owner: -
--

CREATE TABLE elm.doktorantura_proqramlari (
    id integer NOT NULL,
    ad text NOT NULL,
    ixtisas_kodu text,
    seviyye text DEFAULT 'doktorantura'::text NOT NULL,
    muddet_il integer DEFAULT 3,
    qeyd text
);


--
-- Name: TABLE doktorantura_proqramlari; Type: COMMENT; Schema: elm; Owner: -
--

COMMENT ON TABLE elm.doktorantura_proqramlari IS 'Doktorantura ixtisas proqramları';


--
-- Name: doktorantura_proqramlari_id_seq; Type: SEQUENCE; Schema: elm; Owner: -
--

ALTER TABLE elm.doktorantura_proqramlari ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME elm.doktorantura_proqramlari_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: elmi_tedbirler; Type: TABLE; Schema: elm; Owner: -
--

CREATE TABLE elm.elmi_tedbirler (
    id integer NOT NULL,
    ad text NOT NULL,
    tip text DEFAULT 'konfrans'::text NOT NULL,
    tarix date,
    yer text,
    istirakci_sayi integer DEFAULT 0,
    qeyd text
);


--
-- Name: TABLE elmi_tedbirler; Type: COMMENT; Schema: elm; Owner: -
--

COMMENT ON TABLE elm.elmi_tedbirler IS 'Elmi tədbirlər (konfrans, seminar, simpozium)';


--
-- Name: elmi_tedbirler_id_seq; Type: SEQUENCE; Schema: elm; Owner: -
--

ALTER TABLE elm.elmi_tedbirler ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME elm.elmi_tedbirler_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: jurnallar; Type: TABLE; Schema: elm; Owner: -
--

CREATE TABLE elm.jurnallar (
    id integer NOT NULL,
    ad text NOT NULL,
    tip text DEFAULT 'elmi'::text NOT NULL,
    issn text,
    tezlik text,
    tesvir text
);


--
-- Name: TABLE jurnallar; Type: COMMENT; Schema: elm; Owner: -
--

COMMENT ON TABLE elm.jurnallar IS 'ARTİ-nin elmi və metodik jurnalları';


--
-- Name: jurnallar_id_seq; Type: SEQUENCE; Schema: elm; Owner: -
--

ALTER TABLE elm.jurnallar ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME elm.jurnallar_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: meqaleler; Type: TABLE; Schema: elm; Owner: -
--

CREATE TABLE elm.meqaleler (
    id integer NOT NULL,
    jurnal_id integer,
    basliq text NOT NULL,
    muellifler text,
    il integer,
    cild text,
    sehife text,
    doi text,
    qeyd text
);


--
-- Name: TABLE meqaleler; Type: COMMENT; Schema: elm; Owner: -
--

COMMENT ON TABLE elm.meqaleler IS 'Jurnallarda dərc olunan məqalələr';


--
-- Name: meqaleler_id_seq; Type: SEQUENCE; Schema: elm; Owner: -
--

ALTER TABLE elm.meqaleler ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME elm.meqaleler_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: neshrler; Type: TABLE; Schema: elm; Owner: -
--

CREATE TABLE elm.neshrler (
    id integer NOT NULL,
    ad text NOT NULL,
    tip text DEFAULT 'kitab'::text NOT NULL,
    muellif text,
    il integer,
    isbn text,
    say integer DEFAULT 1,
    qeyd text
);


--
-- Name: TABLE neshrler; Type: COMMENT; Schema: elm; Owner: -
--

COMMENT ON TABLE elm.neshrler IS 'Nəşrlər (kitab, dərslik, hesabat)';


--
-- Name: neshrler_id_seq; Type: SEQUENCE; Schema: elm; Owner: -
--

ALTER TABLE elm.neshrler ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME elm.neshrler_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: tedqiqat_istiqametleri; Type: TABLE; Schema: elm; Owner: -
--

CREATE TABLE elm.tedqiqat_istiqametleri (
    id integer NOT NULL,
    ad text NOT NULL,
    tesvir text,
    aktiv boolean DEFAULT true NOT NULL
);


--
-- Name: TABLE tedqiqat_istiqametleri; Type: COMMENT; Schema: elm; Owner: -
--

COMMENT ON TABLE elm.tedqiqat_istiqametleri IS 'Elmi tədqiqat istiqamətləri';


--
-- Name: tedqiqat_istiqametleri_id_seq; Type: SEQUENCE; Schema: elm; Owner: -
--

ALTER TABLE elm.tedqiqat_istiqametleri ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME elm.tedqiqat_istiqametleri_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: tedqiqat_layiheleri; Type: TABLE; Schema: elm; Owner: -
--

CREATE TABLE elm.tedqiqat_layiheleri (
    id integer NOT NULL,
    istiqamet_id integer NOT NULL,
    ad text NOT NULL,
    tesvir text,
    status text DEFAULT 'davam edir'::text NOT NULL,
    rehber_id bigint,
    baslama_tarixi date,
    bitme_tarixi date,
    qeyd text
);


--
-- Name: TABLE tedqiqat_layiheleri; Type: COMMENT; Schema: elm; Owner: -
--

COMMENT ON TABLE elm.tedqiqat_layiheleri IS 'Elmi tədqiqat layihələri';


--
-- Name: tedqiqat_layiheleri_id_seq; Type: SEQUENCE; Schema: elm; Owner: -
--

ALTER TABLE elm.tedqiqat_layiheleri ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME elm.tedqiqat_layiheleri_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: v_doktorant_sayi; Type: VIEW; Schema: elm; Owner: -
--

CREATE VIEW elm.v_doktorant_sayi AS
 SELECT p.id AS proqram_id,
    p.ad AS proqram,
    (count(d.id))::integer AS doktorant_sayi
   FROM (elm.doktorantura_proqramlari p
     LEFT JOIN elm.doktorantlar d ON ((d.proqram_id = p.id)))
  GROUP BY p.id, p.ad;


--
-- Name: emekdaslar; Type: TABLE; Schema: kadrlar; Owner: -
--

CREATE TABLE kadrlar.emekdaslar (
    id bigint NOT NULL,
    ad text NOT NULL,
    soyad text NOT NULL,
    ata_adi text NOT NULL,
    cinsiyyet_id integer NOT NULL,
    dogum_tarixi date,
    vezife_id integer NOT NULL,
    shobe_id integer,
    merkez_id integer,
    email text,
    telefon text,
    is_status_id integer DEFAULT 1 NOT NULL,
    elmi_derece_id integer,
    elmi_ad_id integer,
    ise_baslama date,
    maas numeric(12,2),
    aktiv boolean DEFAULT true NOT NULL,
    yaradilma timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT emekdaslar_maas_check CHECK ((maas >= (0)::numeric))
);


--
-- Name: TABLE emekdaslar; Type: COMMENT; Schema: kadrlar; Owner: -
--

COMMENT ON TABLE kadrlar.emekdaslar IS 'ARTİ əməkdaşları — bütün kadr məlumatı';


--
-- Name: v_tedqiqat_layiheleri; Type: VIEW; Schema: elm; Owner: -
--

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


--
-- Name: emekdaslar_id_seq; Type: SEQUENCE; Schema: kadrlar; Owner: -
--

ALTER TABLE kadrlar.emekdaslar ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME kadrlar.emekdaslar_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: is_tecrubesi; Type: TABLE; Schema: kadrlar; Owner: -
--

CREATE TABLE kadrlar.is_tecrubesi (
    id integer NOT NULL,
    emekdas_id bigint NOT NULL,
    is_yeri text NOT NULL,
    vezife text,
    baslama_tarixi date,
    bitme_tarixi date,
    qeyd text
);


--
-- Name: TABLE is_tecrubesi; Type: COMMENT; Schema: kadrlar; Owner: -
--

COMMENT ON TABLE kadrlar.is_tecrubesi IS 'Əməkdaşların əvvəlki iş yerləri';


--
-- Name: is_tecrubesi_id_seq; Type: SEQUENCE; Schema: kadrlar; Owner: -
--

ALTER TABLE kadrlar.is_tecrubesi ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME kadrlar.is_tecrubesi_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: istifadeciler; Type: TABLE; Schema: kadrlar; Owner: -
--

CREATE TABLE kadrlar.istifadeciler (
    id integer NOT NULL,
    email text NOT NULL,
    parol_hash text NOT NULL,
    ad_soyad text NOT NULL,
    rol text DEFAULT 'baxici'::text NOT NULL,
    emekdas_id bigint,
    aktiv boolean DEFAULT true NOT NULL,
    yaradilma timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: TABLE istifadeciler; Type: COMMENT; Schema: kadrlar; Owner: -
--

COMMENT ON TABLE kadrlar.istifadeciler IS 'Giriş (login) istifadəçiləri və rolları';


--
-- Name: istifadeciler_id_seq; Type: SEQUENCE; Schema: kadrlar; Owner: -
--

ALTER TABLE kadrlar.istifadeciler ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME kadrlar.istifadeciler_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mezuniyyetler; Type: TABLE; Schema: kadrlar; Owner: -
--

CREATE TABLE kadrlar.mezuniyyetler (
    id integer NOT NULL,
    emekdas_id bigint NOT NULL,
    mezuniyyet_tipi text DEFAULT 'illik'::text NOT NULL,
    baslama_tarixi date NOT NULL,
    bitme_tarixi date NOT NULL,
    gun_sayi integer,
    status text DEFAULT 'tesdiqlendi'::text NOT NULL,
    qeyd text,
    CONSTRAINT mezuniyyetler_check CHECK ((bitme_tarixi >= baslama_tarixi)),
    CONSTRAINT mezuniyyetler_gun_sayi_check CHECK ((gun_sayi > 0))
);


--
-- Name: TABLE mezuniyyetler; Type: COMMENT; Schema: kadrlar; Owner: -
--

COMMENT ON TABLE kadrlar.mezuniyyetler IS 'Əməkdaşların məzuniyyətləri';


--
-- Name: mezuniyyetler_id_seq; Type: SEQUENCE; Schema: kadrlar; Owner: -
--

ALTER TABLE kadrlar.mezuniyyetler ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME kadrlar.mezuniyyetler_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: is_statuslari; Type: TABLE; Schema: ortaq; Owner: -
--

CREATE TABLE ortaq.is_statuslari (
    id integer NOT NULL,
    ad text NOT NULL,
    tesvir text,
    aktiv boolean DEFAULT true NOT NULL
);


--
-- Name: TABLE is_statuslari; Type: COMMENT; Schema: ortaq; Owner: -
--

COMMENT ON TABLE ortaq.is_statuslari IS 'Əməkdaşın iş statusu (aktiv, məzuniyyətdə və s.)';


--
-- Name: merkezler; Type: TABLE; Schema: struktur; Owner: -
--

CREATE TABLE struktur.merkezler (
    id integer NOT NULL,
    ad text NOT NULL,
    tip text DEFAULT 'merkez'::text NOT NULL,
    tesvir text,
    unvan text,
    telefon text,
    email text,
    yaradilma_tarixi date,
    aktiv boolean DEFAULT true NOT NULL
);


--
-- Name: TABLE merkezler; Type: COMMENT; Schema: struktur; Owner: -
--

COMMENT ON TABLE struktur.merkezler IS 'ARTİ-nin mərkəzləri, katiblik və funksional blok';


--
-- Name: shobeler; Type: TABLE; Schema: struktur; Owner: -
--

CREATE TABLE struktur.shobeler (
    id integer NOT NULL,
    merkez_id integer NOT NULL,
    ad text NOT NULL,
    qisa_ad text,
    tesvir text,
    telefon text,
    email text,
    aktiv boolean DEFAULT true NOT NULL
);


--
-- Name: TABLE shobeler; Type: COMMENT; Schema: struktur; Owner: -
--

COMMENT ON TABLE struktur.shobeler IS 'Şöbələr — hər biri bir mərkəzə aiddir';


--
-- Name: vezifeler; Type: TABLE; Schema: struktur; Owner: -
--

CREATE TABLE struktur.vezifeler (
    id integer NOT NULL,
    ad text NOT NULL,
    seviyye integer DEFAULT 5 NOT NULL,
    tesvir text
);


--
-- Name: TABLE vezifeler; Type: COMMENT; Schema: struktur; Owner: -
--

COMMENT ON TABLE struktur.vezifeler IS 'Vəzifələr: direktor, müavin, mərkəz rəhbəri, şöbə müdiri...';


--
-- Name: v_emekdas_tam; Type: VIEW; Schema: kadrlar; Owner: -
--

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


--
-- Name: vezife_teyinatlari; Type: TABLE; Schema: kadrlar; Owner: -
--

CREATE TABLE kadrlar.vezife_teyinatlari (
    id integer NOT NULL,
    emekdas_id bigint NOT NULL,
    vezife_id integer NOT NULL,
    shobe_id integer,
    "təyinat_tarixi" date DEFAULT CURRENT_DATE NOT NULL,
    emr_no text,
    status text DEFAULT 'qüvvədədir'::text NOT NULL,
    qeyd text
);


--
-- Name: TABLE vezife_teyinatlari; Type: COMMENT; Schema: kadrlar; Owner: -
--

COMMENT ON TABLE kadrlar.vezife_teyinatlari IS 'Vəzifə təyinatları (kadr əmrlərinin izi)';


--
-- Name: vezife_teyinatlari_id_seq; Type: SEQUENCE; Schema: kadrlar; Owner: -
--

ALTER TABLE kadrlar.vezife_teyinatlari ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME kadrlar.vezife_teyinatlari_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: aktivler; Type: TABLE; Schema: logistika; Owner: -
--

CREATE TABLE logistika.aktivler (
    id integer NOT NULL,
    ad text NOT NULL,
    tip text DEFAULT 'avadanlıq'::text NOT NULL,
    veziyyet text DEFAULT 'yaxşı'::text NOT NULL,
    deyer numeric(14,2) DEFAULT 0,
    alinma_tarixi date,
    qeyd text
);


--
-- Name: TABLE aktivler; Type: COMMENT; Schema: logistika; Owner: -
--

COMMENT ON TABLE logistika.aktivler IS 'Əsas vəsaitlər və avadanlıqlar';


--
-- Name: aktivler_id_seq; Type: SEQUENCE; Schema: logistika; Owner: -
--

ALTER TABLE logistika.aktivler ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME logistika.aktivler_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: binalar; Type: TABLE; Schema: logistika; Owner: -
--

CREATE TABLE logistika.binalar (
    id integer NOT NULL,
    ad text NOT NULL,
    unvan text,
    sahe_m2 integer DEFAULT 0,
    mertebe integer DEFAULT 1,
    qeyd text
);


--
-- Name: TABLE binalar; Type: COMMENT; Schema: logistika; Owner: -
--

COMMENT ON TABLE logistika.binalar IS 'ARTİ-nin binaları və məkanları';


--
-- Name: binalar_id_seq; Type: SEQUENCE; Schema: logistika; Owner: -
--

ALTER TABLE logistika.binalar ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME logistika.binalar_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: it_sistemleri; Type: TABLE; Schema: logistika; Owner: -
--

CREATE TABLE logistika.it_sistemleri (
    id integer NOT NULL,
    ad text NOT NULL,
    tip text DEFAULT 'sayt'::text NOT NULL,
    tesvir text,
    status text DEFAULT 'aktiv'::text NOT NULL,
    qeyd text
);


--
-- Name: TABLE it_sistemleri; Type: COMMENT; Schema: logistika; Owner: -
--

COMMENT ON TABLE logistika.it_sistemleri IS 'İT sistemlər və platformalar';


--
-- Name: it_sistemleri_id_seq; Type: SEQUENCE; Schema: logistika; Owner: -
--

ALTER TABLE logistika.it_sistemleri ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME logistika.it_sistemleri_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: budce; Type: TABLE; Schema: maliyye; Owner: -
--

CREATE TABLE maliyye.budce (
    id integer NOT NULL,
    il integer NOT NULL,
    menbe text DEFAULT 'dovlet'::text NOT NULL,
    mebleg numeric(14,2),
    qeyd text,
    CONSTRAINT budce_mebleg_check CHECK ((mebleg >= (0)::numeric))
);


--
-- Name: TABLE budce; Type: COMMENT; Schema: maliyye; Owner: -
--

COMMENT ON TABLE maliyye.budce IS 'Büdcə sətirləri';


--
-- Name: budce_id_seq; Type: SEQUENCE; Schema: maliyye; Owner: -
--

ALTER TABLE maliyye.budce ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME maliyye.budce_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: maliyye_emeliyyatlari; Type: TABLE; Schema: maliyye; Owner: -
--

CREATE TABLE maliyye.maliyye_emeliyyatlari (
    id integer NOT NULL,
    budce_id integer,
    nov text DEFAULT 'xerc'::text NOT NULL,
    mebleg numeric(14,2),
    tarix date DEFAULT CURRENT_DATE,
    tesvir text,
    qeyd text,
    CONSTRAINT maliyye_emeliyyatlari_mebleg_check CHECK ((mebleg >= (0)::numeric))
);


--
-- Name: TABLE maliyye_emeliyyatlari; Type: COMMENT; Schema: maliyye; Owner: -
--

COMMENT ON TABLE maliyye.maliyye_emeliyyatlari IS 'Maliyyə əməliyyatları';


--
-- Name: maliyye_emeliyyatlari_id_seq; Type: SEQUENCE; Schema: maliyye; Owner: -
--

ALTER TABLE maliyye.maliyye_emeliyyatlari ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME maliyye.maliyye_emeliyyatlari_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: muqavileler; Type: TABLE; Schema: maliyye; Owner: -
--

CREATE TABLE maliyye.muqavileler (
    id integer NOT NULL,
    ad text NOT NULL,
    qarsi_teref text NOT NULL,
    mebleg numeric(14,2),
    baslama_tarixi date,
    bitme_tarixi date,
    status text DEFAULT 'qüvvədədir'::text NOT NULL,
    qeyd text,
    CONSTRAINT muqavileler_mebleg_check CHECK ((mebleg >= (0)::numeric))
);


--
-- Name: TABLE muqavileler; Type: COMMENT; Schema: maliyye; Owner: -
--

COMMENT ON TABLE maliyye.muqavileler IS 'Müqavilələr';


--
-- Name: muqavileler_id_seq; Type: SEQUENCE; Schema: maliyye; Owner: -
--

ALTER TABLE maliyye.muqavileler ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME maliyye.muqavileler_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: satinalmalar; Type: TABLE; Schema: maliyye; Owner: -
--

CREATE TABLE maliyye.satinalmalar (
    id integer NOT NULL,
    ad text NOT NULL,
    nov text DEFAULT 'mal'::text NOT NULL,
    mebleg numeric(14,2),
    tarix date DEFAULT CURRENT_DATE,
    status text DEFAULT 'elan'::text NOT NULL,
    qeyd text,
    CONSTRAINT satinalmalar_mebleg_check CHECK ((mebleg >= (0)::numeric))
);


--
-- Name: TABLE satinalmalar; Type: COMMENT; Schema: maliyye; Owner: -
--

COMMENT ON TABLE maliyye.satinalmalar IS 'Satınalmalar';


--
-- Name: satinalmalar_id_seq; Type: SEQUENCE; Schema: maliyye; Owner: -
--

ALTER TABLE maliyye.satinalmalar ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME maliyye.satinalmalar_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: v_budce_istifadesi; Type: VIEW; Schema: maliyye; Owner: -
--

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


--
-- Name: v_satinalma_veziyyeti; Type: VIEW; Schema: maliyye; Owner: -
--

CREATE VIEW maliyye.v_satinalma_veziyyeti AS
 SELECT status,
    (count(*))::integer AS say,
    COALESCE(sum(mebleg), (0)::numeric) AS umumi_mebleg
   FROM maliyye.satinalmalar
  GROUP BY status;


--
-- Name: metodik_vesaitler; Type: TABLE; Schema: metodika; Owner: -
--

CREATE TABLE metodika.metodik_vesaitler (
    id integer NOT NULL,
    ad text NOT NULL,
    nov text DEFAULT 'vesait'::text NOT NULL,
    fenn text,
    il integer,
    muellif text,
    say integer DEFAULT 100,
    qeyd text
);


--
-- Name: TABLE metodik_vesaitler; Type: COMMENT; Schema: metodika; Owner: -
--

COMMENT ON TABLE metodika.metodik_vesaitler IS 'Metodik vəsaitlər və təlimatlar';


--
-- Name: metodik_vesaitler_id_seq; Type: SEQUENCE; Schema: metodika; Owner: -
--

ALTER TABLE metodika.metodik_vesaitler ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME metodika.metodik_vesaitler_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: metodik_xidmetler; Type: TABLE; Schema: metodika; Owner: -
--

CREATE TABLE metodika.metodik_xidmetler (
    id integer NOT NULL,
    ad text NOT NULL,
    tip text DEFAULT 'meslehet'::text NOT NULL,
    tesvir text,
    status text DEFAULT 'aktiv'::text NOT NULL
);


--
-- Name: TABLE metodik_xidmetler; Type: COMMENT; Schema: metodika; Owner: -
--

COMMENT ON TABLE metodika.metodik_xidmetler IS 'Metodik xidmətlər';


--
-- Name: metodik_xidmetler_id_seq; Type: SEQUENCE; Schema: metodika; Owner: -
--

ALTER TABLE metodika.metodik_xidmetler ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME metodika.metodik_xidmetler_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: cinsiyyet; Type: TABLE; Schema: ortaq; Owner: -
--

CREATE TABLE ortaq.cinsiyyet (
    id integer NOT NULL,
    ad text NOT NULL,
    qisa_ad text NOT NULL
);


--
-- Name: TABLE cinsiyyet; Type: COMMENT; Schema: ortaq; Owner: -
--

COMMENT ON TABLE ortaq.cinsiyyet IS 'Cins lüğəti: Kişi, Qadın, Digər';


--
-- Name: cinsiyyet_id_seq; Type: SEQUENCE; Schema: ortaq; Owner: -
--

ALTER TABLE ortaq.cinsiyyet ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME ortaq.cinsiyyet_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: elmi_adlar; Type: TABLE; Schema: ortaq; Owner: -
--

CREATE TABLE ortaq.elmi_adlar (
    id integer NOT NULL,
    ad text NOT NULL,
    qisa_ad text NOT NULL
);


--
-- Name: TABLE elmi_adlar; Type: COMMENT; Schema: ortaq; Owner: -
--

COMMENT ON TABLE ortaq.elmi_adlar IS 'Elmi adlar: professor, dosent, elmi işçi';


--
-- Name: elmi_adlar_id_seq; Type: SEQUENCE; Schema: ortaq; Owner: -
--

ALTER TABLE ortaq.elmi_adlar ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME ortaq.elmi_adlar_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: elmi_dereceler; Type: TABLE; Schema: ortaq; Owner: -
--

CREATE TABLE ortaq.elmi_dereceler (
    id integer NOT NULL,
    ad text NOT NULL,
    qisa_ad text NOT NULL
);


--
-- Name: TABLE elmi_dereceler; Type: COMMENT; Schema: ortaq; Owner: -
--

COMMENT ON TABLE ortaq.elmi_dereceler IS 'Elmi dərəcələr: bakalavr, magistr, PhD, elmlər doktoru';


--
-- Name: elmi_dereceler_id_seq; Type: SEQUENCE; Schema: ortaq; Owner: -
--

ALTER TABLE ortaq.elmi_dereceler ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME ortaq.elmi_dereceler_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: is_statuslari_id_seq; Type: SEQUENCE; Schema: ortaq; Owner: -
--

ALTER TABLE ortaq.is_statuslari ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME ortaq.is_statuslari_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: beynelxalq_qiymetlendirmeler; Type: TABLE; Schema: qiymetlendirme; Owner: -
--

CREATE TABLE qiymetlendirme.beynelxalq_qiymetlendirmeler (
    id integer NOT NULL,
    ad text NOT NULL,
    qisa_ad text NOT NULL,
    tsikl text,
    il integer,
    istirakci_sayi integer DEFAULT 0,
    status text DEFAULT 'hazirlıq'::text NOT NULL,
    qeyd text
);


--
-- Name: TABLE beynelxalq_qiymetlendirmeler; Type: COMMENT; Schema: qiymetlendirme; Owner: -
--

COMMENT ON TABLE qiymetlendirme.beynelxalq_qiymetlendirmeler IS 'PISA, TIMSS və digər beynəlxalq qiymətləndirmələr';


--
-- Name: beynelxalq_qiymetlendirmeler_id_seq; Type: SEQUENCE; Schema: qiymetlendirme; Owner: -
--

ALTER TABLE qiymetlendirme.beynelxalq_qiymetlendirmeler ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME qiymetlendirme.beynelxalq_qiymetlendirmeler_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: monitorinq_hesabatlari; Type: TABLE; Schema: qiymetlendirme; Owner: -
--

CREATE TABLE qiymetlendirme.monitorinq_hesabatlari (
    id integer NOT NULL,
    ad text NOT NULL,
    nov text DEFAULT 'illik'::text NOT NULL,
    il integer,
    tesvir text,
    status text DEFAULT 'hazirlanir'::text NOT NULL,
    hazirlayan_shobe_id integer,
    qeyd text
);


--
-- Name: TABLE monitorinq_hesabatlari; Type: COMMENT; Schema: qiymetlendirme; Owner: -
--

COMMENT ON TABLE qiymetlendirme.monitorinq_hesabatlari IS 'Monitorinq və təhlil hesabatları';


--
-- Name: monitorinq_hesabatlari_id_seq; Type: SEQUENCE; Schema: qiymetlendirme; Owner: -
--

ALTER TABLE qiymetlendirme.monitorinq_hesabatlari ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME qiymetlendirme.monitorinq_hesabatlari_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: statistik_gostericiler; Type: TABLE; Schema: qiymetlendirme; Owner: -
--

CREATE TABLE qiymetlendirme.statistik_gostericiler (
    id integer NOT NULL,
    gosterici text NOT NULL,
    deyer numeric(14,2),
    vahid text,
    il integer,
    bolge text,
    qeyd text
);


--
-- Name: TABLE statistik_gostericiler; Type: COMMENT; Schema: qiymetlendirme; Owner: -
--

COMMENT ON TABLE qiymetlendirme.statistik_gostericiler IS 'Təhsil üzrə statistik göstəricilər';


--
-- Name: statistik_gostericiler_id_seq; Type: SEQUENCE; Schema: qiymetlendirme; Owner: -
--

ALTER TABLE qiymetlendirme.statistik_gostericiler ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME qiymetlendirme.statistik_gostericiler_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: emrler; Type: TABLE; Schema: sened; Owner: -
--

CREATE TABLE sened.emrler (
    id integer NOT NULL,
    emr_no text NOT NULL,
    tarix date DEFAULT CURRENT_DATE NOT NULL,
    movzu text NOT NULL,
    imzalayan text,
    qeyd text
);


--
-- Name: TABLE emrler; Type: COMMENT; Schema: sened; Owner: -
--

COMMENT ON TABLE sened.emrler IS 'İnstitut üzrə əmrlər';


--
-- Name: emrler_id_seq; Type: SEQUENCE; Schema: sened; Owner: -
--

ALTER TABLE sened.emrler ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME sened.emrler_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: sened_novleri; Type: TABLE; Schema: sened; Owner: -
--

CREATE TABLE sened.sened_novleri (
    id integer NOT NULL,
    ad text NOT NULL,
    tesvir text
);


--
-- Name: TABLE sened_novleri; Type: COMMENT; Schema: sened; Owner: -
--

COMMENT ON TABLE sened.sened_novleri IS 'Sənəd növləri lüğəti';


--
-- Name: sened_novleri_id_seq; Type: SEQUENCE; Schema: sened; Owner: -
--

ALTER TABLE sened.sened_novleri ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME sened.sened_novleri_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: senedler; Type: TABLE; Schema: sened; Owner: -
--

CREATE TABLE sened.senedler (
    id integer NOT NULL,
    nov_id integer NOT NULL,
    nomre text,
    tarix date DEFAULT CURRENT_DATE NOT NULL,
    movzu text NOT NULL,
    gonderen text,
    alan text,
    status text DEFAULT 'qeydiyyatda'::text NOT NULL,
    qeyd text
);


--
-- Name: TABLE senedler; Type: COMMENT; Schema: sened; Owner: -
--

COMMENT ON TABLE sened.senedler IS 'Ümumi sənədlər (yazışmalar)';


--
-- Name: senedler_id_seq; Type: SEQUENCE; Schema: sened; Owner: -
--

ALTER TABLE sened.senedler ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME sened.senedler_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: elmi_shura_iclaslari; Type: TABLE; Schema: struktur; Owner: -
--

CREATE TABLE struktur.elmi_shura_iclaslari (
    id integer NOT NULL,
    iclas_tarixi date NOT NULL,
    novu text DEFAULT 'novbeti'::text NOT NULL,
    gundelik text,
    kecirildiyi_yer text,
    protokol_no text,
    qeyd text
);


--
-- Name: TABLE elmi_shura_iclaslari; Type: COMMENT; Schema: struktur; Owner: -
--

COMMENT ON TABLE struktur.elmi_shura_iclaslari IS 'Elmi Şura iclaslarının qeydiyyatı';


--
-- Name: elmi_shura_iclaslari_id_seq; Type: SEQUENCE; Schema: struktur; Owner: -
--

ALTER TABLE struktur.elmi_shura_iclaslari ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME struktur.elmi_shura_iclaslari_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: elmi_shura_qerarlari; Type: TABLE; Schema: struktur; Owner: -
--

CREATE TABLE struktur.elmi_shura_qerarlari (
    id integer NOT NULL,
    iclas_id integer NOT NULL,
    qerar_no text,
    qerar_metni text NOT NULL,
    icraci_shobe_id integer,
    son_tarix date,
    status text DEFAULT 'icrada'::text NOT NULL,
    qeyd text
);


--
-- Name: TABLE elmi_shura_qerarlari; Type: COMMENT; Schema: struktur; Owner: -
--

COMMENT ON TABLE struktur.elmi_shura_qerarlari IS 'Elmi Şura qərarları və icra vəziyyəti';


--
-- Name: elmi_shura_qerarlari_id_seq; Type: SEQUENCE; Schema: struktur; Owner: -
--

ALTER TABLE struktur.elmi_shura_qerarlari ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME struktur.elmi_shura_qerarlari_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: elmi_shura_uzvleri; Type: TABLE; Schema: struktur; Owner: -
--

CREATE TABLE struktur.elmi_shura_uzvleri (
    id integer NOT NULL,
    emekdas_id bigint,
    ad_soyad text NOT NULL,
    vezife_id integer,
    elmi_derece_id integer,
    elmi_ad_id integer,
    status text DEFAULT 'uzv'::text NOT NULL,
    qosulma_tarixi date,
    aktiv boolean DEFAULT true NOT NULL
);


--
-- Name: TABLE elmi_shura_uzvleri; Type: COMMENT; Schema: struktur; Owner: -
--

COMMENT ON TABLE struktur.elmi_shura_uzvleri IS 'Elmi Şura üzvləri (sədr, katib, üzvlər)';


--
-- Name: elmi_shura_uzvleri_id_seq; Type: SEQUENCE; Schema: struktur; Owner: -
--

ALTER TABLE struktur.elmi_shura_uzvleri ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME struktur.elmi_shura_uzvleri_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: merkezler_id_seq; Type: SEQUENCE; Schema: struktur; Owner: -
--

ALTER TABLE struktur.merkezler ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME struktur.merkezler_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: rehberlik; Type: TABLE; Schema: struktur; Owner: -
--

CREATE TABLE struktur.rehberlik (
    id integer NOT NULL,
    emekdas_id bigint NOT NULL,
    vezife_id integer NOT NULL,
    merkez_id integer,
    sira integer DEFAULT 99 NOT NULL,
    tesvir text,
    aktiv boolean DEFAULT true NOT NULL
);


--
-- Name: TABLE rehberlik; Type: COMMENT; Schema: struktur; Owner: -
--

COMMENT ON TABLE struktur.rehberlik IS 'Rəhbərlik heyəti: direktor və direktor müavinləri';


--
-- Name: rehberlik_id_seq; Type: SEQUENCE; Schema: struktur; Owner: -
--

ALTER TABLE struktur.rehberlik ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME struktur.rehberlik_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: shobeler_id_seq; Type: SEQUENCE; Schema: struktur; Owner: -
--

ALTER TABLE struktur.shobeler ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME struktur.shobeler_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: v_merkez_shobe_sayi; Type: VIEW; Schema: struktur; Owner: -
--

CREATE VIEW struktur.v_merkez_shobe_sayi AS
 SELECT m.id AS merkez_id,
    m.ad AS merkez,
    (count(s.id))::integer AS shobe_sayi
   FROM (struktur.merkezler m
     LEFT JOIN struktur.shobeler s ON ((s.merkez_id = m.id)))
  GROUP BY m.id, m.ad;


--
-- Name: vezifeler_id_seq; Type: SEQUENCE; Schema: struktur; Owner: -
--

ALTER TABLE struktur.vezifeler ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME struktur.vezifeler_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: imtahanlar; Type: TABLE; Schema: tehsil; Owner: -
--

CREATE TABLE tehsil.imtahanlar (
    id integer NOT NULL,
    ad text NOT NULL,
    tip text DEFAULT 'sertifikasiya'::text NOT NULL,
    tarix date,
    istirakci_sayi integer DEFAULT 0,
    qeyd text
);


--
-- Name: TABLE imtahanlar; Type: COMMENT; Schema: tehsil; Owner: -
--

COMMENT ON TABLE tehsil.imtahanlar IS 'İmtahanlar (sertifikasiya, MİQ, qəbul)';


--
-- Name: imtahanlar_id_seq; Type: SEQUENCE; Schema: tehsil; Owner: -
--

ALTER TABLE tehsil.imtahanlar ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME tehsil.imtahanlar_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: sertifikasiya; Type: TABLE; Schema: tehsil; Owner: -
--

CREATE TABLE tehsil.sertifikasiya (
    id integer NOT NULL,
    emekdas_id bigint,
    ad_soyad text NOT NULL,
    tip text DEFAULT 'müəllim'::text NOT NULL,
    imtahan_tarixi date,
    bal numeric(5,1),
    netice text DEFAULT 'keçdi'::text NOT NULL,
    sertifikat_no text,
    qeyd text,
    CONSTRAINT sertifikasiya_bal_check CHECK ((bal >= (0)::numeric))
);


--
-- Name: TABLE sertifikasiya; Type: COMMENT; Schema: tehsil; Owner: -
--

COMMENT ON TABLE tehsil.sertifikasiya IS 'Müəllim sertifikasiyası nəticələri';


--
-- Name: sertifikasiya_id_seq; Type: SEQUENCE; Schema: tehsil; Owner: -
--

ALTER TABLE tehsil.sertifikasiya ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME tehsil.sertifikasiya_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: telim_istirakcilari; Type: TABLE; Schema: tehsil; Owner: -
--

CREATE TABLE tehsil.telim_istirakcilari (
    id integer NOT NULL,
    qrup_id integer NOT NULL,
    ad text NOT NULL,
    soyad text NOT NULL,
    ata_adi text NOT NULL,
    is_yeri text,
    sertifikat_no text,
    status text DEFAULT 'bitirdi'::text NOT NULL,
    qeyd text
);


--
-- Name: TABLE telim_istirakcilari; Type: COMMENT; Schema: tehsil; Owner: -
--

COMMENT ON TABLE tehsil.telim_istirakcilari IS 'Təlim iştirakçıları (müəllimlər)';


--
-- Name: telim_istirakcilari_id_seq; Type: SEQUENCE; Schema: tehsil; Owner: -
--

ALTER TABLE tehsil.telim_istirakcilari ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME tehsil.telim_istirakcilari_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: telim_proqramlari; Type: TABLE; Schema: tehsil; Owner: -
--

CREATE TABLE tehsil.telim_proqramlari (
    id integer NOT NULL,
    ad text NOT NULL,
    kateqoriya text DEFAULT 'umumi'::text NOT NULL,
    saat integer DEFAULT 20,
    hedef_qrup text,
    tesvir text
);


--
-- Name: TABLE telim_proqramlari; Type: COMMENT; Schema: tehsil; Owner: -
--

COMMENT ON TABLE tehsil.telim_proqramlari IS 'Təlim proqramları (peşəkar inkişaf kursları)';


--
-- Name: telim_proqramlari_id_seq; Type: SEQUENCE; Schema: tehsil; Owner: -
--

ALTER TABLE tehsil.telim_proqramlari ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME tehsil.telim_proqramlari_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: telim_qruplari; Type: TABLE; Schema: tehsil; Owner: -
--

CREATE TABLE tehsil.telim_qruplari (
    id integer NOT NULL,
    proqram_id integer NOT NULL,
    ad text NOT NULL,
    telimci_id bigint,
    baslama_tarixi date,
    bitme_tarixi date,
    status text DEFAULT 'planlasdirilir'::text NOT NULL,
    qeyd text
);


--
-- Name: TABLE telim_qruplari; Type: COMMENT; Schema: tehsil; Owner: -
--

COMMENT ON TABLE tehsil.telim_qruplari IS 'Təlim qrupları';


--
-- Name: telim_qruplari_id_seq; Type: SEQUENCE; Schema: tehsil; Owner: -
--

ALTER TABLE tehsil.telim_qruplari ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME tehsil.telim_qruplari_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: v_telim_qrup_istirakci_sayi; Type: VIEW; Schema: tehsil; Owner: -
--

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


--
-- Name: ai_promptlar ai_promptlar_pkey; Type: CONSTRAINT; Schema: ai; Owner: -
--

ALTER TABLE ONLY ai.ai_promptlar
    ADD CONSTRAINT ai_promptlar_pkey PRIMARY KEY (id);


--
-- Name: ai_sorghular ai_sorghular_pkey; Type: CONSTRAINT; Schema: ai; Owner: -
--

ALTER TABLE ONLY ai.ai_sorghular
    ADD CONSTRAINT ai_sorghular_pkey PRIMARY KEY (id);


--
-- Name: embeddingler embeddingler_pkey; Type: CONSTRAINT; Schema: ai; Owner: -
--

ALTER TABLE ONLY ai.embeddingler
    ADD CONSTRAINT embeddingler_pkey PRIMARY KEY (id);


--
-- Name: audit_log audit_log_pkey; Type: CONSTRAINT; Schema: audit; Owner: -
--

ALTER TABLE ONLY audit.audit_log
    ADD CONSTRAINT audit_log_pkey PRIMARY KEY (id);


--
-- Name: doktorantlar doktorantlar_pkey; Type: CONSTRAINT; Schema: elm; Owner: -
--

ALTER TABLE ONLY elm.doktorantlar
    ADD CONSTRAINT doktorantlar_pkey PRIMARY KEY (id);


--
-- Name: doktorantura_proqramlari doktorantura_proqramlari_pkey; Type: CONSTRAINT; Schema: elm; Owner: -
--

ALTER TABLE ONLY elm.doktorantura_proqramlari
    ADD CONSTRAINT doktorantura_proqramlari_pkey PRIMARY KEY (id);


--
-- Name: elmi_tedbirler elmi_tedbirler_pkey; Type: CONSTRAINT; Schema: elm; Owner: -
--

ALTER TABLE ONLY elm.elmi_tedbirler
    ADD CONSTRAINT elmi_tedbirler_pkey PRIMARY KEY (id);


--
-- Name: jurnallar jurnallar_ad_key; Type: CONSTRAINT; Schema: elm; Owner: -
--

ALTER TABLE ONLY elm.jurnallar
    ADD CONSTRAINT jurnallar_ad_key UNIQUE (ad);


--
-- Name: jurnallar jurnallar_pkey; Type: CONSTRAINT; Schema: elm; Owner: -
--

ALTER TABLE ONLY elm.jurnallar
    ADD CONSTRAINT jurnallar_pkey PRIMARY KEY (id);


--
-- Name: meqaleler meqaleler_pkey; Type: CONSTRAINT; Schema: elm; Owner: -
--

ALTER TABLE ONLY elm.meqaleler
    ADD CONSTRAINT meqaleler_pkey PRIMARY KEY (id);


--
-- Name: neshrler neshrler_pkey; Type: CONSTRAINT; Schema: elm; Owner: -
--

ALTER TABLE ONLY elm.neshrler
    ADD CONSTRAINT neshrler_pkey PRIMARY KEY (id);


--
-- Name: tedqiqat_istiqametleri tedqiqat_istiqametleri_ad_key; Type: CONSTRAINT; Schema: elm; Owner: -
--

ALTER TABLE ONLY elm.tedqiqat_istiqametleri
    ADD CONSTRAINT tedqiqat_istiqametleri_ad_key UNIQUE (ad);


--
-- Name: tedqiqat_istiqametleri tedqiqat_istiqametleri_pkey; Type: CONSTRAINT; Schema: elm; Owner: -
--

ALTER TABLE ONLY elm.tedqiqat_istiqametleri
    ADD CONSTRAINT tedqiqat_istiqametleri_pkey PRIMARY KEY (id);


--
-- Name: tedqiqat_layiheleri tedqiqat_layiheleri_pkey; Type: CONSTRAINT; Schema: elm; Owner: -
--

ALTER TABLE ONLY elm.tedqiqat_layiheleri
    ADD CONSTRAINT tedqiqat_layiheleri_pkey PRIMARY KEY (id);


--
-- Name: emekdaslar emekdaslar_email_key; Type: CONSTRAINT; Schema: kadrlar; Owner: -
--

ALTER TABLE ONLY kadrlar.emekdaslar
    ADD CONSTRAINT emekdaslar_email_key UNIQUE (email);


--
-- Name: emekdaslar emekdaslar_pkey; Type: CONSTRAINT; Schema: kadrlar; Owner: -
--

ALTER TABLE ONLY kadrlar.emekdaslar
    ADD CONSTRAINT emekdaslar_pkey PRIMARY KEY (id);


--
-- Name: is_tecrubesi is_tecrubesi_pkey; Type: CONSTRAINT; Schema: kadrlar; Owner: -
--

ALTER TABLE ONLY kadrlar.is_tecrubesi
    ADD CONSTRAINT is_tecrubesi_pkey PRIMARY KEY (id);


--
-- Name: istifadeciler istifadeciler_email_key; Type: CONSTRAINT; Schema: kadrlar; Owner: -
--

ALTER TABLE ONLY kadrlar.istifadeciler
    ADD CONSTRAINT istifadeciler_email_key UNIQUE (email);


--
-- Name: istifadeciler istifadeciler_pkey; Type: CONSTRAINT; Schema: kadrlar; Owner: -
--

ALTER TABLE ONLY kadrlar.istifadeciler
    ADD CONSTRAINT istifadeciler_pkey PRIMARY KEY (id);


--
-- Name: mezuniyyetler mezuniyyetler_pkey; Type: CONSTRAINT; Schema: kadrlar; Owner: -
--

ALTER TABLE ONLY kadrlar.mezuniyyetler
    ADD CONSTRAINT mezuniyyetler_pkey PRIMARY KEY (id);


--
-- Name: vezife_teyinatlari vezife_teyinatlari_pkey; Type: CONSTRAINT; Schema: kadrlar; Owner: -
--

ALTER TABLE ONLY kadrlar.vezife_teyinatlari
    ADD CONSTRAINT vezife_teyinatlari_pkey PRIMARY KEY (id);


--
-- Name: aktivler aktivler_pkey; Type: CONSTRAINT; Schema: logistika; Owner: -
--

ALTER TABLE ONLY logistika.aktivler
    ADD CONSTRAINT aktivler_pkey PRIMARY KEY (id);


--
-- Name: binalar binalar_pkey; Type: CONSTRAINT; Schema: logistika; Owner: -
--

ALTER TABLE ONLY logistika.binalar
    ADD CONSTRAINT binalar_pkey PRIMARY KEY (id);


--
-- Name: it_sistemleri it_sistemleri_pkey; Type: CONSTRAINT; Schema: logistika; Owner: -
--

ALTER TABLE ONLY logistika.it_sistemleri
    ADD CONSTRAINT it_sistemleri_pkey PRIMARY KEY (id);


--
-- Name: budce budce_pkey; Type: CONSTRAINT; Schema: maliyye; Owner: -
--

ALTER TABLE ONLY maliyye.budce
    ADD CONSTRAINT budce_pkey PRIMARY KEY (id);


--
-- Name: maliyye_emeliyyatlari maliyye_emeliyyatlari_pkey; Type: CONSTRAINT; Schema: maliyye; Owner: -
--

ALTER TABLE ONLY maliyye.maliyye_emeliyyatlari
    ADD CONSTRAINT maliyye_emeliyyatlari_pkey PRIMARY KEY (id);


--
-- Name: muqavileler muqavileler_pkey; Type: CONSTRAINT; Schema: maliyye; Owner: -
--

ALTER TABLE ONLY maliyye.muqavileler
    ADD CONSTRAINT muqavileler_pkey PRIMARY KEY (id);


--
-- Name: satinalmalar satinalmalar_pkey; Type: CONSTRAINT; Schema: maliyye; Owner: -
--

ALTER TABLE ONLY maliyye.satinalmalar
    ADD CONSTRAINT satinalmalar_pkey PRIMARY KEY (id);


--
-- Name: metodik_vesaitler metodik_vesaitler_pkey; Type: CONSTRAINT; Schema: metodika; Owner: -
--

ALTER TABLE ONLY metodika.metodik_vesaitler
    ADD CONSTRAINT metodik_vesaitler_pkey PRIMARY KEY (id);


--
-- Name: metodik_xidmetler metodik_xidmetler_pkey; Type: CONSTRAINT; Schema: metodika; Owner: -
--

ALTER TABLE ONLY metodika.metodik_xidmetler
    ADD CONSTRAINT metodik_xidmetler_pkey PRIMARY KEY (id);


--
-- Name: cinsiyyet cinsiyyet_ad_key; Type: CONSTRAINT; Schema: ortaq; Owner: -
--

ALTER TABLE ONLY ortaq.cinsiyyet
    ADD CONSTRAINT cinsiyyet_ad_key UNIQUE (ad);


--
-- Name: cinsiyyet cinsiyyet_pkey; Type: CONSTRAINT; Schema: ortaq; Owner: -
--

ALTER TABLE ONLY ortaq.cinsiyyet
    ADD CONSTRAINT cinsiyyet_pkey PRIMARY KEY (id);


--
-- Name: elmi_adlar elmi_adlar_ad_key; Type: CONSTRAINT; Schema: ortaq; Owner: -
--

ALTER TABLE ONLY ortaq.elmi_adlar
    ADD CONSTRAINT elmi_adlar_ad_key UNIQUE (ad);


--
-- Name: elmi_adlar elmi_adlar_pkey; Type: CONSTRAINT; Schema: ortaq; Owner: -
--

ALTER TABLE ONLY ortaq.elmi_adlar
    ADD CONSTRAINT elmi_adlar_pkey PRIMARY KEY (id);


--
-- Name: elmi_dereceler elmi_dereceler_ad_key; Type: CONSTRAINT; Schema: ortaq; Owner: -
--

ALTER TABLE ONLY ortaq.elmi_dereceler
    ADD CONSTRAINT elmi_dereceler_ad_key UNIQUE (ad);


--
-- Name: elmi_dereceler elmi_dereceler_pkey; Type: CONSTRAINT; Schema: ortaq; Owner: -
--

ALTER TABLE ONLY ortaq.elmi_dereceler
    ADD CONSTRAINT elmi_dereceler_pkey PRIMARY KEY (id);


--
-- Name: is_statuslari is_statuslari_ad_key; Type: CONSTRAINT; Schema: ortaq; Owner: -
--

ALTER TABLE ONLY ortaq.is_statuslari
    ADD CONSTRAINT is_statuslari_ad_key UNIQUE (ad);


--
-- Name: is_statuslari is_statuslari_pkey; Type: CONSTRAINT; Schema: ortaq; Owner: -
--

ALTER TABLE ONLY ortaq.is_statuslari
    ADD CONSTRAINT is_statuslari_pkey PRIMARY KEY (id);


--
-- Name: beynelxalq_qiymetlendirmeler beynelxalq_qiymetlendirmeler_pkey; Type: CONSTRAINT; Schema: qiymetlendirme; Owner: -
--

ALTER TABLE ONLY qiymetlendirme.beynelxalq_qiymetlendirmeler
    ADD CONSTRAINT beynelxalq_qiymetlendirmeler_pkey PRIMARY KEY (id);


--
-- Name: monitorinq_hesabatlari monitorinq_hesabatlari_pkey; Type: CONSTRAINT; Schema: qiymetlendirme; Owner: -
--

ALTER TABLE ONLY qiymetlendirme.monitorinq_hesabatlari
    ADD CONSTRAINT monitorinq_hesabatlari_pkey PRIMARY KEY (id);


--
-- Name: statistik_gostericiler statistik_gostericiler_pkey; Type: CONSTRAINT; Schema: qiymetlendirme; Owner: -
--

ALTER TABLE ONLY qiymetlendirme.statistik_gostericiler
    ADD CONSTRAINT statistik_gostericiler_pkey PRIMARY KEY (id);


--
-- Name: emrler emrler_pkey; Type: CONSTRAINT; Schema: sened; Owner: -
--

ALTER TABLE ONLY sened.emrler
    ADD CONSTRAINT emrler_pkey PRIMARY KEY (id);


--
-- Name: sened_novleri sened_novleri_ad_key; Type: CONSTRAINT; Schema: sened; Owner: -
--

ALTER TABLE ONLY sened.sened_novleri
    ADD CONSTRAINT sened_novleri_ad_key UNIQUE (ad);


--
-- Name: sened_novleri sened_novleri_pkey; Type: CONSTRAINT; Schema: sened; Owner: -
--

ALTER TABLE ONLY sened.sened_novleri
    ADD CONSTRAINT sened_novleri_pkey PRIMARY KEY (id);


--
-- Name: senedler senedler_pkey; Type: CONSTRAINT; Schema: sened; Owner: -
--

ALTER TABLE ONLY sened.senedler
    ADD CONSTRAINT senedler_pkey PRIMARY KEY (id);


--
-- Name: elmi_shura_iclaslari elmi_shura_iclaslari_pkey; Type: CONSTRAINT; Schema: struktur; Owner: -
--

ALTER TABLE ONLY struktur.elmi_shura_iclaslari
    ADD CONSTRAINT elmi_shura_iclaslari_pkey PRIMARY KEY (id);


--
-- Name: elmi_shura_qerarlari elmi_shura_qerarlari_pkey; Type: CONSTRAINT; Schema: struktur; Owner: -
--

ALTER TABLE ONLY struktur.elmi_shura_qerarlari
    ADD CONSTRAINT elmi_shura_qerarlari_pkey PRIMARY KEY (id);


--
-- Name: elmi_shura_uzvleri elmi_shura_uzvleri_pkey; Type: CONSTRAINT; Schema: struktur; Owner: -
--

ALTER TABLE ONLY struktur.elmi_shura_uzvleri
    ADD CONSTRAINT elmi_shura_uzvleri_pkey PRIMARY KEY (id);


--
-- Name: merkezler merkezler_ad_key; Type: CONSTRAINT; Schema: struktur; Owner: -
--

ALTER TABLE ONLY struktur.merkezler
    ADD CONSTRAINT merkezler_ad_key UNIQUE (ad);


--
-- Name: merkezler merkezler_pkey; Type: CONSTRAINT; Schema: struktur; Owner: -
--

ALTER TABLE ONLY struktur.merkezler
    ADD CONSTRAINT merkezler_pkey PRIMARY KEY (id);


--
-- Name: rehberlik rehberlik_emekdas_id_key; Type: CONSTRAINT; Schema: struktur; Owner: -
--

ALTER TABLE ONLY struktur.rehberlik
    ADD CONSTRAINT rehberlik_emekdas_id_key UNIQUE (emekdas_id);


--
-- Name: rehberlik rehberlik_pkey; Type: CONSTRAINT; Schema: struktur; Owner: -
--

ALTER TABLE ONLY struktur.rehberlik
    ADD CONSTRAINT rehberlik_pkey PRIMARY KEY (id);


--
-- Name: shobeler shobeler_merkez_id_ad_key; Type: CONSTRAINT; Schema: struktur; Owner: -
--

ALTER TABLE ONLY struktur.shobeler
    ADD CONSTRAINT shobeler_merkez_id_ad_key UNIQUE (merkez_id, ad);


--
-- Name: shobeler shobeler_pkey; Type: CONSTRAINT; Schema: struktur; Owner: -
--

ALTER TABLE ONLY struktur.shobeler
    ADD CONSTRAINT shobeler_pkey PRIMARY KEY (id);


--
-- Name: vezifeler vezifeler_ad_key; Type: CONSTRAINT; Schema: struktur; Owner: -
--

ALTER TABLE ONLY struktur.vezifeler
    ADD CONSTRAINT vezifeler_ad_key UNIQUE (ad);


--
-- Name: vezifeler vezifeler_pkey; Type: CONSTRAINT; Schema: struktur; Owner: -
--

ALTER TABLE ONLY struktur.vezifeler
    ADD CONSTRAINT vezifeler_pkey PRIMARY KEY (id);


--
-- Name: imtahanlar imtahanlar_pkey; Type: CONSTRAINT; Schema: tehsil; Owner: -
--

ALTER TABLE ONLY tehsil.imtahanlar
    ADD CONSTRAINT imtahanlar_pkey PRIMARY KEY (id);


--
-- Name: sertifikasiya sertifikasiya_pkey; Type: CONSTRAINT; Schema: tehsil; Owner: -
--

ALTER TABLE ONLY tehsil.sertifikasiya
    ADD CONSTRAINT sertifikasiya_pkey PRIMARY KEY (id);


--
-- Name: telim_istirakcilari telim_istirakcilari_pkey; Type: CONSTRAINT; Schema: tehsil; Owner: -
--

ALTER TABLE ONLY tehsil.telim_istirakcilari
    ADD CONSTRAINT telim_istirakcilari_pkey PRIMARY KEY (id);


--
-- Name: telim_proqramlari telim_proqramlari_pkey; Type: CONSTRAINT; Schema: tehsil; Owner: -
--

ALTER TABLE ONLY tehsil.telim_proqramlari
    ADD CONSTRAINT telim_proqramlari_pkey PRIMARY KEY (id);


--
-- Name: telim_qruplari telim_qruplari_pkey; Type: CONSTRAINT; Schema: tehsil; Owner: -
--

ALTER TABLE ONLY tehsil.telim_qruplari
    ADD CONSTRAINT telim_qruplari_pkey PRIMARY KEY (id);


--
-- Name: idx_ai_sorghu_vaxt; Type: INDEX; Schema: ai; Owner: -
--

CREATE INDEX idx_ai_sorghu_vaxt ON ai.ai_sorghular USING btree (vaxt);


--
-- Name: idx_audit_cedvel; Type: INDEX; Schema: audit; Owner: -
--

CREATE INDEX idx_audit_cedvel ON audit.audit_log USING btree (cedvel_adi);


--
-- Name: idx_doktorantlar_proqram; Type: INDEX; Schema: elm; Owner: -
--

CREATE INDEX idx_doktorantlar_proqram ON elm.doktorantlar USING btree (proqram_id);


--
-- Name: idx_doktorantlar_status; Type: INDEX; Schema: elm; Owner: -
--

CREATE INDEX idx_doktorantlar_status ON elm.doktorantlar USING btree (status);


--
-- Name: idx_meqaleler_jurnal; Type: INDEX; Schema: elm; Owner: -
--

CREATE INDEX idx_meqaleler_jurnal ON elm.meqaleler USING btree (jurnal_id);


--
-- Name: idx_neshr_il; Type: INDEX; Schema: elm; Owner: -
--

CREATE INDEX idx_neshr_il ON elm.neshrler USING btree (il);


--
-- Name: idx_tedqiqat_layihe_istiqamet; Type: INDEX; Schema: elm; Owner: -
--

CREATE INDEX idx_tedqiqat_layihe_istiqamet ON elm.tedqiqat_layiheleri USING btree (istiqamet_id);


--
-- Name: idx_tedqiqat_layihe_rehber; Type: INDEX; Schema: elm; Owner: -
--

CREATE INDEX idx_tedqiqat_layihe_rehber ON elm.tedqiqat_layiheleri USING btree (rehber_id);


--
-- Name: idx_tedqiqat_layihe_status; Type: INDEX; Schema: elm; Owner: -
--

CREATE INDEX idx_tedqiqat_layihe_status ON elm.tedqiqat_layiheleri USING btree (status);


--
-- Name: idx_emekdaslar_email; Type: INDEX; Schema: kadrlar; Owner: -
--

CREATE INDEX idx_emekdaslar_email ON kadrlar.emekdaslar USING btree (email);


--
-- Name: idx_emekdaslar_shobe; Type: INDEX; Schema: kadrlar; Owner: -
--

CREATE INDEX idx_emekdaslar_shobe ON kadrlar.emekdaslar USING btree (shobe_id);


--
-- Name: idx_emekdaslar_soyad; Type: INDEX; Schema: kadrlar; Owner: -
--

CREATE INDEX idx_emekdaslar_soyad ON kadrlar.emekdaslar USING btree (soyad);


--
-- Name: idx_emekdaslar_vezife; Type: INDEX; Schema: kadrlar; Owner: -
--

CREATE INDEX idx_emekdaslar_vezife ON kadrlar.emekdaslar USING btree (vezife_id);


--
-- Name: idx_aktiv_tip; Type: INDEX; Schema: logistika; Owner: -
--

CREATE INDEX idx_aktiv_tip ON logistika.aktivler USING btree (tip);


--
-- Name: idx_budce_il; Type: INDEX; Schema: maliyye; Owner: -
--

CREATE INDEX idx_budce_il ON maliyye.budce USING btree (il);


--
-- Name: idx_emeliyyat_budce; Type: INDEX; Schema: maliyye; Owner: -
--

CREATE INDEX idx_emeliyyat_budce ON maliyye.maliyye_emeliyyatlari USING btree (budce_id);


--
-- Name: idx_muqavile_status; Type: INDEX; Schema: maliyye; Owner: -
--

CREATE INDEX idx_muqavile_status ON maliyye.muqavileler USING btree (status);


--
-- Name: idx_satinalma_status; Type: INDEX; Schema: maliyye; Owner: -
--

CREATE INDEX idx_satinalma_status ON maliyye.satinalmalar USING btree (status);


--
-- Name: idx_beynelxalq_qisa_ad; Type: INDEX; Schema: qiymetlendirme; Owner: -
--

CREATE INDEX idx_beynelxalq_qisa_ad ON qiymetlendirme.beynelxalq_qiymetlendirmeler USING btree (qisa_ad);


--
-- Name: idx_monitorinq_il; Type: INDEX; Schema: qiymetlendirme; Owner: -
--

CREATE INDEX idx_monitorinq_il ON qiymetlendirme.monitorinq_hesabatlari USING btree (il);


--
-- Name: idx_statistik_il; Type: INDEX; Schema: qiymetlendirme; Owner: -
--

CREATE INDEX idx_statistik_il ON qiymetlendirme.statistik_gostericiler USING btree (il);


--
-- Name: idx_senedler_nov; Type: INDEX; Schema: sened; Owner: -
--

CREATE INDEX idx_senedler_nov ON sened.senedler USING btree (nov_id);


--
-- Name: idx_senedler_tarix; Type: INDEX; Schema: sened; Owner: -
--

CREATE INDEX idx_senedler_tarix ON sened.senedler USING btree (tarix);


--
-- Name: idx_shobeler_merkez; Type: INDEX; Schema: struktur; Owner: -
--

CREATE INDEX idx_shobeler_merkez ON struktur.shobeler USING btree (merkez_id);


--
-- Name: idx_sertifikasiya_netice; Type: INDEX; Schema: tehsil; Owner: -
--

CREATE INDEX idx_sertifikasiya_netice ON tehsil.sertifikasiya USING btree (netice);


--
-- Name: idx_sertifikasiya_tarix; Type: INDEX; Schema: tehsil; Owner: -
--

CREATE INDEX idx_sertifikasiya_tarix ON tehsil.sertifikasiya USING btree (imtahan_tarixi);


--
-- Name: idx_telim_istirakci_qrup; Type: INDEX; Schema: tehsil; Owner: -
--

CREATE INDEX idx_telim_istirakci_qrup ON tehsil.telim_istirakcilari USING btree (qrup_id);


--
-- Name: idx_telim_qruplari_proqram; Type: INDEX; Schema: tehsil; Owner: -
--

CREATE INDEX idx_telim_qruplari_proqram ON tehsil.telim_qruplari USING btree (proqram_id);


--
-- Name: tedqiqat_layiheleri trg_tedqiqat_layiheleri_audit; Type: TRIGGER; Schema: elm; Owner: -
--

CREATE TRIGGER trg_tedqiqat_layiheleri_audit AFTER INSERT OR DELETE OR UPDATE ON elm.tedqiqat_layiheleri FOR EACH ROW EXECUTE FUNCTION audit.fn_audit_yaz();


--
-- Name: emekdaslar trg_emekdaslar_audit; Type: TRIGGER; Schema: kadrlar; Owner: -
--

CREATE TRIGGER trg_emekdaslar_audit AFTER INSERT OR DELETE OR UPDATE ON kadrlar.emekdaslar FOR EACH ROW EXECUTE FUNCTION audit.fn_audit_yaz();


--
-- Name: mezuniyyetler trg_mezuniyyet_gun_sayi; Type: TRIGGER; Schema: kadrlar; Owner: -
--

CREATE TRIGGER trg_mezuniyyet_gun_sayi BEFORE INSERT OR UPDATE ON kadrlar.mezuniyyetler FOR EACH ROW EXECUTE FUNCTION kadrlar.fn_gun_sayi_hesabla();


--
-- Name: budce trg_budce_audit; Type: TRIGGER; Schema: maliyye; Owner: -
--

CREATE TRIGGER trg_budce_audit AFTER INSERT OR DELETE OR UPDATE ON maliyye.budce FOR EACH ROW EXECUTE FUNCTION audit.fn_audit_yaz();


--
-- Name: satinalmalar trg_satinalmalar_audit; Type: TRIGGER; Schema: maliyye; Owner: -
--

CREATE TRIGGER trg_satinalmalar_audit AFTER INSERT OR DELETE OR UPDATE ON maliyye.satinalmalar FOR EACH ROW EXECUTE FUNCTION audit.fn_audit_yaz();


--
-- Name: doktorantlar doktorantlar_proqram_id_fkey; Type: FK CONSTRAINT; Schema: elm; Owner: -
--

ALTER TABLE ONLY elm.doktorantlar
    ADD CONSTRAINT doktorantlar_proqram_id_fkey FOREIGN KEY (proqram_id) REFERENCES elm.doktorantura_proqramlari(id);


--
-- Name: doktorantlar doktorantlar_rehber_id_fkey; Type: FK CONSTRAINT; Schema: elm; Owner: -
--

ALTER TABLE ONLY elm.doktorantlar
    ADD CONSTRAINT doktorantlar_rehber_id_fkey FOREIGN KEY (rehber_id) REFERENCES kadrlar.emekdaslar(id);


--
-- Name: meqaleler meqaleler_jurnal_id_fkey; Type: FK CONSTRAINT; Schema: elm; Owner: -
--

ALTER TABLE ONLY elm.meqaleler
    ADD CONSTRAINT meqaleler_jurnal_id_fkey FOREIGN KEY (jurnal_id) REFERENCES elm.jurnallar(id);


--
-- Name: tedqiqat_layiheleri tedqiqat_layiheleri_istiqamet_id_fkey; Type: FK CONSTRAINT; Schema: elm; Owner: -
--

ALTER TABLE ONLY elm.tedqiqat_layiheleri
    ADD CONSTRAINT tedqiqat_layiheleri_istiqamet_id_fkey FOREIGN KEY (istiqamet_id) REFERENCES elm.tedqiqat_istiqametleri(id);


--
-- Name: tedqiqat_layiheleri tedqiqat_layiheleri_rehber_id_fkey; Type: FK CONSTRAINT; Schema: elm; Owner: -
--

ALTER TABLE ONLY elm.tedqiqat_layiheleri
    ADD CONSTRAINT tedqiqat_layiheleri_rehber_id_fkey FOREIGN KEY (rehber_id) REFERENCES kadrlar.emekdaslar(id);


--
-- Name: emekdaslar emekdaslar_cinsiyyet_id_fkey; Type: FK CONSTRAINT; Schema: kadrlar; Owner: -
--

ALTER TABLE ONLY kadrlar.emekdaslar
    ADD CONSTRAINT emekdaslar_cinsiyyet_id_fkey FOREIGN KEY (cinsiyyet_id) REFERENCES ortaq.cinsiyyet(id);


--
-- Name: emekdaslar emekdaslar_elmi_ad_id_fkey; Type: FK CONSTRAINT; Schema: kadrlar; Owner: -
--

ALTER TABLE ONLY kadrlar.emekdaslar
    ADD CONSTRAINT emekdaslar_elmi_ad_id_fkey FOREIGN KEY (elmi_ad_id) REFERENCES ortaq.elmi_adlar(id);


--
-- Name: emekdaslar emekdaslar_elmi_derece_id_fkey; Type: FK CONSTRAINT; Schema: kadrlar; Owner: -
--

ALTER TABLE ONLY kadrlar.emekdaslar
    ADD CONSTRAINT emekdaslar_elmi_derece_id_fkey FOREIGN KEY (elmi_derece_id) REFERENCES ortaq.elmi_dereceler(id);


--
-- Name: emekdaslar emekdaslar_is_status_id_fkey; Type: FK CONSTRAINT; Schema: kadrlar; Owner: -
--

ALTER TABLE ONLY kadrlar.emekdaslar
    ADD CONSTRAINT emekdaslar_is_status_id_fkey FOREIGN KEY (is_status_id) REFERENCES ortaq.is_statuslari(id);


--
-- Name: emekdaslar emekdaslar_merkez_id_fkey; Type: FK CONSTRAINT; Schema: kadrlar; Owner: -
--

ALTER TABLE ONLY kadrlar.emekdaslar
    ADD CONSTRAINT emekdaslar_merkez_id_fkey FOREIGN KEY (merkez_id) REFERENCES struktur.merkezler(id);


--
-- Name: emekdaslar emekdaslar_shobe_id_fkey; Type: FK CONSTRAINT; Schema: kadrlar; Owner: -
--

ALTER TABLE ONLY kadrlar.emekdaslar
    ADD CONSTRAINT emekdaslar_shobe_id_fkey FOREIGN KEY (shobe_id) REFERENCES struktur.shobeler(id);


--
-- Name: emekdaslar emekdaslar_vezife_id_fkey; Type: FK CONSTRAINT; Schema: kadrlar; Owner: -
--

ALTER TABLE ONLY kadrlar.emekdaslar
    ADD CONSTRAINT emekdaslar_vezife_id_fkey FOREIGN KEY (vezife_id) REFERENCES struktur.vezifeler(id);


--
-- Name: is_tecrubesi is_tecrubesi_emekdas_id_fkey; Type: FK CONSTRAINT; Schema: kadrlar; Owner: -
--

ALTER TABLE ONLY kadrlar.is_tecrubesi
    ADD CONSTRAINT is_tecrubesi_emekdas_id_fkey FOREIGN KEY (emekdas_id) REFERENCES kadrlar.emekdaslar(id) ON DELETE CASCADE;


--
-- Name: istifadeciler istifadeciler_emekdas_id_fkey; Type: FK CONSTRAINT; Schema: kadrlar; Owner: -
--

ALTER TABLE ONLY kadrlar.istifadeciler
    ADD CONSTRAINT istifadeciler_emekdas_id_fkey FOREIGN KEY (emekdas_id) REFERENCES kadrlar.emekdaslar(id);


--
-- Name: mezuniyyetler mezuniyyetler_emekdas_id_fkey; Type: FK CONSTRAINT; Schema: kadrlar; Owner: -
--

ALTER TABLE ONLY kadrlar.mezuniyyetler
    ADD CONSTRAINT mezuniyyetler_emekdas_id_fkey FOREIGN KEY (emekdas_id) REFERENCES kadrlar.emekdaslar(id) ON DELETE CASCADE;


--
-- Name: vezife_teyinatlari vezife_teyinatlari_emekdas_id_fkey; Type: FK CONSTRAINT; Schema: kadrlar; Owner: -
--

ALTER TABLE ONLY kadrlar.vezife_teyinatlari
    ADD CONSTRAINT vezife_teyinatlari_emekdas_id_fkey FOREIGN KEY (emekdas_id) REFERENCES kadrlar.emekdaslar(id) ON DELETE CASCADE;


--
-- Name: vezife_teyinatlari vezife_teyinatlari_shobe_id_fkey; Type: FK CONSTRAINT; Schema: kadrlar; Owner: -
--

ALTER TABLE ONLY kadrlar.vezife_teyinatlari
    ADD CONSTRAINT vezife_teyinatlari_shobe_id_fkey FOREIGN KEY (shobe_id) REFERENCES struktur.shobeler(id);


--
-- Name: vezife_teyinatlari vezife_teyinatlari_vezife_id_fkey; Type: FK CONSTRAINT; Schema: kadrlar; Owner: -
--

ALTER TABLE ONLY kadrlar.vezife_teyinatlari
    ADD CONSTRAINT vezife_teyinatlari_vezife_id_fkey FOREIGN KEY (vezife_id) REFERENCES struktur.vezifeler(id);


--
-- Name: maliyye_emeliyyatlari maliyye_emeliyyatlari_budce_id_fkey; Type: FK CONSTRAINT; Schema: maliyye; Owner: -
--

ALTER TABLE ONLY maliyye.maliyye_emeliyyatlari
    ADD CONSTRAINT maliyye_emeliyyatlari_budce_id_fkey FOREIGN KEY (budce_id) REFERENCES maliyye.budce(id);


--
-- Name: monitorinq_hesabatlari monitorinq_hesabatlari_hazirlayan_shobe_id_fkey; Type: FK CONSTRAINT; Schema: qiymetlendirme; Owner: -
--

ALTER TABLE ONLY qiymetlendirme.monitorinq_hesabatlari
    ADD CONSTRAINT monitorinq_hesabatlari_hazirlayan_shobe_id_fkey FOREIGN KEY (hazirlayan_shobe_id) REFERENCES struktur.shobeler(id);


--
-- Name: senedler senedler_nov_id_fkey; Type: FK CONSTRAINT; Schema: sened; Owner: -
--

ALTER TABLE ONLY sened.senedler
    ADD CONSTRAINT senedler_nov_id_fkey FOREIGN KEY (nov_id) REFERENCES sened.sened_novleri(id);


--
-- Name: elmi_shura_qerarlari elmi_shura_qerarlari_iclas_id_fkey; Type: FK CONSTRAINT; Schema: struktur; Owner: -
--

ALTER TABLE ONLY struktur.elmi_shura_qerarlari
    ADD CONSTRAINT elmi_shura_qerarlari_iclas_id_fkey FOREIGN KEY (iclas_id) REFERENCES struktur.elmi_shura_iclaslari(id) ON DELETE CASCADE;


--
-- Name: elmi_shura_qerarlari elmi_shura_qerarlari_icraci_shobe_id_fkey; Type: FK CONSTRAINT; Schema: struktur; Owner: -
--

ALTER TABLE ONLY struktur.elmi_shura_qerarlari
    ADD CONSTRAINT elmi_shura_qerarlari_icraci_shobe_id_fkey FOREIGN KEY (icraci_shobe_id) REFERENCES struktur.shobeler(id);


--
-- Name: elmi_shura_uzvleri elmi_shura_uzvleri_elmi_ad_id_fkey; Type: FK CONSTRAINT; Schema: struktur; Owner: -
--

ALTER TABLE ONLY struktur.elmi_shura_uzvleri
    ADD CONSTRAINT elmi_shura_uzvleri_elmi_ad_id_fkey FOREIGN KEY (elmi_ad_id) REFERENCES ortaq.elmi_adlar(id);


--
-- Name: elmi_shura_uzvleri elmi_shura_uzvleri_elmi_derece_id_fkey; Type: FK CONSTRAINT; Schema: struktur; Owner: -
--

ALTER TABLE ONLY struktur.elmi_shura_uzvleri
    ADD CONSTRAINT elmi_shura_uzvleri_elmi_derece_id_fkey FOREIGN KEY (elmi_derece_id) REFERENCES ortaq.elmi_dereceler(id);


--
-- Name: elmi_shura_uzvleri elmi_shura_uzvleri_emekdas_id_fkey; Type: FK CONSTRAINT; Schema: struktur; Owner: -
--

ALTER TABLE ONLY struktur.elmi_shura_uzvleri
    ADD CONSTRAINT elmi_shura_uzvleri_emekdas_id_fkey FOREIGN KEY (emekdas_id) REFERENCES kadrlar.emekdaslar(id);


--
-- Name: elmi_shura_uzvleri elmi_shura_uzvleri_vezife_id_fkey; Type: FK CONSTRAINT; Schema: struktur; Owner: -
--

ALTER TABLE ONLY struktur.elmi_shura_uzvleri
    ADD CONSTRAINT elmi_shura_uzvleri_vezife_id_fkey FOREIGN KEY (vezife_id) REFERENCES struktur.vezifeler(id);


--
-- Name: rehberlik rehberlik_emekdas_id_fkey; Type: FK CONSTRAINT; Schema: struktur; Owner: -
--

ALTER TABLE ONLY struktur.rehberlik
    ADD CONSTRAINT rehberlik_emekdas_id_fkey FOREIGN KEY (emekdas_id) REFERENCES kadrlar.emekdaslar(id) ON DELETE CASCADE;


--
-- Name: rehberlik rehberlik_merkez_id_fkey; Type: FK CONSTRAINT; Schema: struktur; Owner: -
--

ALTER TABLE ONLY struktur.rehberlik
    ADD CONSTRAINT rehberlik_merkez_id_fkey FOREIGN KEY (merkez_id) REFERENCES struktur.merkezler(id);


--
-- Name: rehberlik rehberlik_vezife_id_fkey; Type: FK CONSTRAINT; Schema: struktur; Owner: -
--

ALTER TABLE ONLY struktur.rehberlik
    ADD CONSTRAINT rehberlik_vezife_id_fkey FOREIGN KEY (vezife_id) REFERENCES struktur.vezifeler(id);


--
-- Name: shobeler shobeler_merkez_id_fkey; Type: FK CONSTRAINT; Schema: struktur; Owner: -
--

ALTER TABLE ONLY struktur.shobeler
    ADD CONSTRAINT shobeler_merkez_id_fkey FOREIGN KEY (merkez_id) REFERENCES struktur.merkezler(id) ON DELETE CASCADE;


--
-- Name: sertifikasiya sertifikasiya_emekdas_id_fkey; Type: FK CONSTRAINT; Schema: tehsil; Owner: -
--

ALTER TABLE ONLY tehsil.sertifikasiya
    ADD CONSTRAINT sertifikasiya_emekdas_id_fkey FOREIGN KEY (emekdas_id) REFERENCES kadrlar.emekdaslar(id);


--
-- Name: telim_istirakcilari telim_istirakcilari_qrup_id_fkey; Type: FK CONSTRAINT; Schema: tehsil; Owner: -
--

ALTER TABLE ONLY tehsil.telim_istirakcilari
    ADD CONSTRAINT telim_istirakcilari_qrup_id_fkey FOREIGN KEY (qrup_id) REFERENCES tehsil.telim_qruplari(id);


--
-- Name: telim_qruplari telim_qruplari_proqram_id_fkey; Type: FK CONSTRAINT; Schema: tehsil; Owner: -
--

ALTER TABLE ONLY tehsil.telim_qruplari
    ADD CONSTRAINT telim_qruplari_proqram_id_fkey FOREIGN KEY (proqram_id) REFERENCES tehsil.telim_proqramlari(id);


--
-- Name: telim_qruplari telim_qruplari_telimci_id_fkey; Type: FK CONSTRAINT; Schema: tehsil; Owner: -
--

ALTER TABLE ONLY tehsil.telim_qruplari
    ADD CONSTRAINT telim_qruplari_telimci_id_fkey FOREIGN KEY (telimci_id) REFERENCES kadrlar.emekdaslar(id);


--
-- PostgreSQL database dump complete
--

\unrestrict ZuCCv71ouSVfW6LkiQpwQVcvo5SKQ9OfgkcXtgRSQKNhQ9fvgsiX0I41vFkc7rq

