function lda_vis(k, dt){

    //Object.keys(dtm_data)

    var ldavis_data = dtm_data[k][dt];

    if (dt!='' && k>0){
      document.getElementById('ldavis_el604422654636080886007232696').innerHTML = ""; //comentar esto si se quiere visualizar todo en una página
      // parent.location.hash("topic=0&lambda=1&term=");
    }
    function verifyorder() {

      //?#topic=2&lambda=0&term=  solucionar tema url, minimo ?#
        function LDAvis_load_lib(url, callback){
          var s = document.createElement('script');
          s.src = url;
          s.async = true;
          s.onreadystatechange = s.onload = callback;
          s.onerror = function(){console.warn("failed to load library " + url);};
          document.getElementsByTagName("head")[0].appendChild(s);
        }

        if(typeof(LDAvis) !== "undefined"){
           // already loaded: just create the visualization
           !function(LDAvis){
               new LDAvis("#" + "ldavis_el604422654636080886007232696", ldavis_data);

           }(LDAvis);
        }else if(typeof define === "function" && define.amd){
           // require.js is available: use it to load d3/LDAvis
           require.config({paths: {d3: "https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min"}});
           require(["d3"], function(d3){
              window.d3 = d3;
              LDAvis_load_lib("https://cdn.rawgit.com/bmabey/pyLDAvis/files/ldavis.v1.0.0.js", function(){
                new LDAvis("#" + "ldavis_el604422654636080886007232696", ldavis_data);
              });
            });
        }else{
            // require.js not available: dynamically load d3 & LDAvis
            LDAvis_load_lib("https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js", function(){
                 LDAvis_load_lib("https://cdn.rawgit.com/bmabey/pyLDAvis/files/ldavis.v1.0.0.js", function(){
                         new LDAvis("#" + "ldavis_el604422654636080886007232696", ldavis_data);
                    })
                 });
        }

    }
    verifyorder()



  }
