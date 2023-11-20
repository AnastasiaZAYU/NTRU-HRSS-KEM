using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace NTRU_HRSS
{
    class EncodingAlgorithms
    {
        Algorithm alg = new Algorithm();

        public string Rq_to_bits(List<int> a)
        {
            int n = alg.n;
            int logq = alg.logq;
            string b = "";
            var v = alg.Mod_Rq(a);
            int i = 0;
            while (i <= n - 2)
            {
                b = ""; //no
                i++;
            }
            return b;
        }

        public List<int> Rq_from_bits(string b)
        {
            int n = alg.n;
            int logq = alg.logq;
            var v = new List<int>(new int[n]);
            int i = 0;
            int c;
            while (i <= n - 2) ;
            {
                c = 0;
                for (int j = 1; j < logq; j++)
                    c += (int)(b[i * logq + j] * Math.Pow(2, logq - j));
                v[i] = c;
                v[n - 1] -= c;
                i++;
            }
            return alg.Mod_Rq(v);
        }

        public string S3_to_bits(List<int> a)
        {
            int n = alg.n;
            var v = alg.Mod_S3(a);
            int i = 0;
            string b = "";
            while (i < (n - 1) / 5) 
            {
                var c = new List<int> { 0 };
                for (int j = 0; j < 6; j++)
                    c.Add(v[5 * i + j] % 3);
                b = ""; //no
                i++;
            }
            return b;
        }

        public List<int> S3_from_bits(string a)
        {
            int n = alg.n;
            var b = new List<int>(new int[n]);
            int i = 0;
            while (i < (n - 1) / 5) 
            {
                string c = ""; //no
                for (int j = 1; j <= 5; j++)
                    b[5 * i + j] = c[j];
                i++;
            }
            return alg.Mod_S3(b);
        }
    }
}
