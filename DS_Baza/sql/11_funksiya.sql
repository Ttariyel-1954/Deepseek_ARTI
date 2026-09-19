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
