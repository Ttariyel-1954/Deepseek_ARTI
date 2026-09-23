LAYIHE="${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"

# ⚠️ Test mötərizə içindədir — `exit` yalnız bu bloku dayandırır,
#    Terminal sessiyanız açıq qalır. (bash və zsh ilə işləyir)
(
cd "${LAYIHE:-$HOME/Deepseek_ARTI/DS_Backend}"
unset DATABASE_URL PGHOST
export PGPASSWORD="${PGPASSWORD:-arti_secret_2025}"

echo "── Pasportun mənbələri ──"
psql -U arti_user -d arti_baza -c "
  SELECT 'telim_istirakcilari' AS cedvel, count(*) AS setir FROM tehsil.telim_istirakcilari
  UNION ALL SELECT 'telim_qruplari',      count(*) FROM tehsil.telim_qruplari
  UNION ALL SELECT 'telim_proqramlari',   count(*) FROM tehsil.telim_proqramlari
  UNION ALL SELECT 'sertifikasiya',       count(*) FROM tehsil.sertifikasiya" | sed 's/^/  /'

echo "── Bağlayıcı açar: sertifikat_no ──"
psql -U arti_user -d arti_baza -c "
  SELECT i.ad || ' ' || i.soyad AS sahib, i.sertifikat_no,
         q.ad AS qrup, p.ad AS proqram, s.netice, s.bal
  FROM tehsil.telim_istirakcilari i
  LEFT JOIN tehsil.telim_qruplari    q ON q.id = i.qrup_id
  LEFT JOIN tehsil.telim_proqramlari p ON p.id = q.proqram_id
  LEFT JOIN tehsil.sertifikasiya     s ON s.sertifikat_no = i.sertifikat_no
  ORDER BY i.id LIMIT 5" | sed 's/^/  /'

echo "── Nə üçün ad üzrə deyil, NÖMRƏ üzrə? ──"
psql -U arti_user -d arti_baza -tA -c "
  SELECT '  eyni adlı sertifikasiya qeydi: ' || count(*)
  FROM (SELECT ad_soyad FROM tehsil.sertifikasiya GROUP BY ad_soyad HAVING count(*) > 1) x"
echo "  → ad təkrarlana bilər, sertifikat nömrəsi UNİKALdır"
)
