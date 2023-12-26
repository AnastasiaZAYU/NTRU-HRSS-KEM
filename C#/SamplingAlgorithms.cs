using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace NTRU_HRSS
{
    class SamplingAlgorithms
    {
        Algorithm alg = new Algorithm();
        ExternallyAlgorithms ext = new ExternallyAlgorithms();

        public List<int> Sample_T(byte[] seed, byte[] domain)
        {
            int n = alg.n;
            int k = alg.k;
            var v = new List<int>(new int[n - 1]);
            int i = 0;
            int l = 2 * k * (n - 1);
            var b = ext.SHAKE128(seed.Concat(domain).ToArray(), l); //no
            while (i < n - 1) 
            {
                for (int j = 1; j <= k; j++)
                    v[i] += ((int)b[2 * k * i + j] - (int)b[2 * k * i + k + j]);
                i++;
            }
            return alg.Mod_S3(v);
        }

        public List<int> Sample_Tplus(byte[] seed, byte[] domain)
        {
            int n = alg.n;
            var v = Sample_T(seed, domain);
            int t = 0, s = 0;
            for (int j = 1; j <= n - 2; j++) 
                t += v[j] * v[j - 1];
            if (t < 0) s = -1;
            else s = 1;
            int i = 0;
            while (i < n - 2) 
            {
                v[i] = (s * v[i]) % n;
                i += 2;
            }
            return alg.Mod_S3(v);
        }
    }
}
