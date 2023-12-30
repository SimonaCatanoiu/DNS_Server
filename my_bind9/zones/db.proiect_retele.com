$TTL    604800
@   IN  SOA proiect_retele.com. root.proiect_retele.com. (
                  2     ; Serial
             604800     ; Refresh
              86400     ; Retry
            2419200     ; Expire
             604800 )   ; Negative Cache TTL
;
; NS records
IN        NS      ns1.proiect_retele.com.
; A records
ns1.proiect_retele.com.    IN      A      172.20.0.2
site.proiect_retele.com.   IN      A      172.20.0.2
mail.proiect_retele.com.   IN      A      172.20.0.3
proiect_retele.com.        IN      MX     10  mail.retele3.mta.ro.
