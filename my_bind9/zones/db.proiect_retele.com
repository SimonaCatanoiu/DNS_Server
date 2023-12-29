$TTL    604800
@   IN  SOA proiect_retele.com. root.proiect_retele.com. (
                  2       ; Serial
             604800     ; Refresh
              86400     ; Retry
            2419200     ; Expire
             604800 )   ; Negative Cache TTL
;
; name servers - NS records
  IN        NS      ns1.proiect_retele.com.

; name servers - A records
ns1.proiect_retele.com.    IN      A      172.20.0.2
site.proiect_retele.com.    IN      A      172.20.0.2
