using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace NTRU_HRSS
{
    class KeyEncapsulationMechanism
    {
        ArithmeticAlgorithms ari = new ArithmeticAlgorithms();
        SamplingAlgorithms sa = new SamplingAlgorithms();
        Algorithm alg = new Algorithm();

   /*     public void Generate_Key()
        {
            var seed = alg.RandomStringBits(seed_bits);
            var f = Generate_Private_Key(seed);
            //fp = S3_inverse(f);
            //var h = Generate_Public_Key(seed, f);
            //packed_public_key = Rq_to_bits(h);
            //packed_private_key = S3_to_bits(f) || S3_to_bits(fp);
            //return packed_public_key, packed_private_key;
        }*/

        private List<int> Generate_Private_Key(byte[] seed)
        {
            byte[] domf = BitConverter.GetBytes(0x0100000000000000);
            var f = sa.Sample_Tplus(seed, domf);
            return f;
        }

        private List<int> Generate_Public_Key(byte[] seed, List<int> f)
        {
            int n = alg.n;
            byte[] domg = BitConverter.GetBytes(0x0200000000000000);
            var v0 = sa.Sample_Tplus(seed, domg);
            var g = ari.S3_to_Zx(v0);
            var v1 = ari.Sq_inverse(f);
            var fq = ari.Sq_to_Zx(v1);
            var v2 = alg.Multiply(g, fq, n);
            var x1 = new List<int> { -3, 3 };
            v2 = alg.Multiply(x1, v2, n);
            return alg.Mod_Rq(v2);
        }
    }
}
