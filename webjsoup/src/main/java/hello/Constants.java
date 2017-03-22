package hello;

import java.util.regex.Pattern;

/**
 * Created by smartkit on 22/03/2017.
 */
public class Constants {
    private static final String ROOT_URL = "http://www.newsmth.net";
    private static final String BASE_URL = "http://www.newsmth.net/nForum/board/CouponsLife";

    private static final String AM_ROOT_URL = "https://www.amazon.cn/";
    public static final String AM_BASE_URL = "https://www.amazon.cn/gp/goldbox/all-deals";
    private static final String AMZ_PAGE_URL = "https://www.amazon.cn/gp/goldbox/ref=gbps_ftr_s-4_68d9_page_2?gb_f_GB-SUPPLE=page:2,sortOrder:BY_SCORE,dealsPerPage:18&pf_rd_p=fd0b439a-1761-4f65-859a-d880c95c68d9&pf_rd_s=slot-4&pf_rd_t=701&pf_rd_i=gb_main&pf_rd_m=A1AJ19PSB66TGU&pf_rd_r=JAMNNEB0MEJEE42CJ40N";

    private static final String[] KEYS = {"亚马逊", "白条", "亚麻", "闪付", "ofo", "摩拜", "手慢无", "物美", "翼支付", "菜鸟", "大毛", "小毛", "超市", "jd", "华夏", "z秒"};
    private static final String[] AUTHOR = {"keeker"};
    private static final String[] EXCLUDE = {"吗", "?", "？", "为什么", "求", "如何", "怎么样", "咨询", "为啥"};

    private static final Pattern IMAGE_EXTENSIONS = Pattern.compile(".*\\.(bmp|gif|jpg|png)$");
}
