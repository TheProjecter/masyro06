      // Para realizar el rollover de las imagenes 
      function imageOn (el) {
            var str_switch = "on";
            chr = el.src.lastIndexOf("-") + 1;
            period = el.src.lastIndexOf(".");

            el.src = "" + el.src.substring(0, chr) + str_switch + el.src.substring(period, el.src.length);
            return true;
      }

 	   function imageClick (el) {
            var str_switch = "click";
            chr = el.src.lastIndexOf("-") + 1;
            period = el.src.lastIndexOf(".");

            el.src = "" + el.src.substring(0, chr) + str_switch + el.src.substring(period, el.src.length);
            return true;
      }
      function imageOff (el) {
            var str_switch = "off";
            chr = el.src.lastIndexOf("-") + 1;
            period = el.src.lastIndexOf(".");

            el.src = "" + el.src.substring(0, chr) + str_switch + el.src.substring(period, el.src.length);
            return true;
      }
      