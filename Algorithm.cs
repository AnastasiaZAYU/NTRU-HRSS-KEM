using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace NTRU_HRSS
{
    class Algorithm
    {
        int n = 701;
        int q = 8192;

        public List<int> Mod_Sq(List<int> a)
        {
            List<int> S = new List<int>();
            for (int i = 0; i < n; i++)
                S.Add(1);
            a = RemainderDivision(a, S, n);
            for (int i = 0; i < a.Count; i++)
            {
                a[i] %= q;
                if (a[i] > q / 2 - 1) a[i] -= q;
            }
            return a;
        }

        public List<int> Mod_S3(List<int> a)
        {
            List<int> S = new List<int>();
            for (int i = 0; i < n; i++)
                S.Add(1);
            a = RemainderDivision(a, S, n);
            for (int i = 0; i < a.Count; i++)
            {
                a[i] %= 3;
                if (a[i] == 2) a[i] -= 3;
            }
            return a;
        }

        public List<int> Mod_S2(List<int> a)
        {
            List<int> S = new List<int>();
            for (int i = 0; i < n; i++)
                S.Add(1);
            a = RemainderDivision(a, S, n);
            for (int i = 0; i < a.Count; i++)
                a[i] %= 2;
            return a;
        }

        public List<int> Mod_Rq(List<int> a)
        {
            List<int> R = new List<int> { n - 1 };
            for (int i = 0; i < n - 1; i++)
                R.Add(0);
            R.Add(1);
            a = RemainderDivision(a, R, n);
            for (int i = 0; i < a.Count; i++)
            {
                a[i] %= q;
                if (a[i] > q / 2 - 1) a[i] -= q;
            }
            return a;
        }

        private List<int> RemainderDivision(List<int> a, List<int> b, int mod)
        {
            while (a.Count >= b.Count)
            {
                var c = b.ToList();
                c.InsertRange(0, Enumerable.Repeat(0, a.Count - c.Count));
                int coef = a.Last();
                for (int i = 0; i < a.Count; i++)
                    a[i] = (mod + (a[i] - coef * c[i])) % mod;
                foreach (int i in a)
                    Console.Write("{0} ", i);
                Console.WriteLine();
                while (a.Count > 0 && a.Last() == 0)
                    a.RemoveAt(a.Count - 1);
            }
            return a;
        }

    }
}
