using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace NTRU_HRSS
{
    class ArithmeticAlgorithms
    {
        Algorithm alg = new Algorithm();

        public List<int> S3_to_R(List<int> a)
        {
            var n = alg.n;
            var x1 = new List<int> { n - 1, 1 };
            var v0 = S3_inverse(x1); // no
            var v1 = alg.Multiply(v0, a, n);
            var v2 = S3_to_Zx(v1);
            var b = alg.Multiply(x1, v2, n);
            return b;
        }

        public List<int> S3_to_Zx(List<int> a)
        {
            return alg.Mod_S3(a);
        }

        public List<int> Sq_to_Zx(List<int> a)
        {
            return alg.Mod_Sq(a);
        }

        public List<int> Rq_to_Zx(List<int> a)
        {
            return alg.Mod_Rq(a);
        }

        public List<int> S2_inverse(List<int> a)
        {
            return a; //inverse
        }

        public List<int> S3_inverse(List<int> a)
        {
            return a; //inverse
        }

        public List<int> Sq_inverse(List<int> a)
        {
            int q = alg.q;
            var v0 = S2_inverse(a);
            int t = 2;
            while (t < q) 
            {
                //v0 = alg.Mod_Sq(alg.Multiply(v0,))
            }
            return a; //inverse
        }
    }
}
