using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Security.Cryptography;

namespace NTRU_HRSS
{
    class Algorithm
    {
        public int n = 701;
        public int k = 2;
        int seed_bits = 256;
        int coin_bits = 256;
        int shared_key_bits = 256;
        public int logq = 13;
        public int q = 8192;
        int s3_packed_bits = 1120;
        int owcpa_public_key_bits = 9100;
        int owcpa_private_key_bits = 2240;
        int owcpa_ciphertext_bits = 9100;
        int cca_public_key_bits = 9100;
        int cca_private_key_bits = 10220;
        int cca_ciphertext_bits = 10220;

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

        private List<int> Mod_S2(List<int> a)
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

        public List<int> RemainderDivision(List<int> a, List<int> b, int mod)
        {
            while (a.Count >= b.Count)
            {
                var c = b.ToList();
                c.InsertRange(0, Enumerable.Repeat(0, a.Count - c.Count));
                int coef = a.Last();
                for (int i = 0; i < a.Count; i++)
                    a[i] = (mod + (a[i] - coef * c[i])) % mod;
                while (a.Count > 0 && a.Last() == 0)
                    a.RemoveAt(a.Count - 1);
            }
            return a;
        }

        public List<int> Multiply(List<int> a, List<int> b, int mod)
        {
            int a_n = a.Count;
            int b_n = b.Count;
            int size = a_n + b_n - 1;
            List<int> result = new List<int>(new int[size]);
            for (int i = 0; i < a_n; i++)
            {
                for (int j = 0; j < b_n; j++)
                {
                    result[i + j] += a[i] * b[j];
                    result[i + j] %= mod;
                }
            }
            while (result.Count > 0 && result.Last() == 0)
                result.RemoveAt(result.Count - 1);
            return result;
        }

        public List<int> Subtract(List<int> a, List<int> b, int mod)
        {
            var c = new List<int>();
            int maxlen = Math.Max(a.Count, b.Count);
            int minlen = Math.Min(a.Count, b.Count);
            for (int i = 0; i < minlen; i++)
                c.Add((mod + (a[i] - b[i]) % mod) % mod);
            if (a.Count > b.Count)
            {
                for (int i = minlen; i < maxlen; i++)
                    c.Add(a[i]);
            }
            else if (b.Count > a.Count)
            {
                for (int i = minlen; i < maxlen; i++)
                    c.Add(mod - b[i]);
            }
            return c;
        }

        public List<int> Addition(List<int> a, List<int> b, int mod)
        {
            var c = new List<int>();
            if (a.Count < b.Count) c = b.ToList();
            else c = b.ToList();
            for (int i = 0; i < Math.Min(a.Count, b.Count); i++)
                c[i] = (a[i] + b[i]) % mod;
            return c;
        }

        public byte[] RandomStringBits(int len)
        {
            using (RNGCryptoServiceProvider rng = new RNGCryptoServiceProvider())
            {
                byte[] randomBytes = new byte[len / 8];
                rng.GetBytes(randomBytes);
                return randomBytes;
            }
        }

        public void Print(List<int> list)
        {
            foreach (int i in list)
                Console.Write("{0} ", i);
            Console.WriteLine();
        }

    }
}
