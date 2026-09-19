CREATE TRIGGER trg_tedqiqat_layiheleri_audit AFTER INSERT OR DELETE OR UPDATE ON elm.tedqiqat_layiheleri FOR EACH ROW EXECUTE FUNCTION audit.fn_audit_yaz();
CREATE TRIGGER trg_emekdaslar_audit AFTER INSERT OR DELETE OR UPDATE ON kadrlar.emekdaslar FOR EACH ROW EXECUTE FUNCTION audit.fn_audit_yaz();
CREATE TRIGGER trg_mezuniyyet_gun_sayi BEFORE INSERT OR UPDATE ON kadrlar.mezuniyyetler FOR EACH ROW EXECUTE FUNCTION kadrlar.fn_gun_sayi_hesabla();
CREATE TRIGGER trg_budce_audit AFTER INSERT OR DELETE OR UPDATE ON maliyye.budce FOR EACH ROW EXECUTE FUNCTION audit.fn_audit_yaz();
CREATE TRIGGER trg_satinalmalar_audit AFTER INSERT OR DELETE OR UPDATE ON maliyye.satinalmalar FOR EACH ROW EXECUTE FUNCTION audit.fn_audit_yaz();
