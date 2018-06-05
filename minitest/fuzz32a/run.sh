for i in $(seq 0 15) ; do
    export ZIA_DST=$i; make && mv build build_fb1.0-fb2.$ZIA_DST
done

