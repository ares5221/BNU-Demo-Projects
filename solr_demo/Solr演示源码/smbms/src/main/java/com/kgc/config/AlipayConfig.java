package com.kgc.config;

/**
 * 支付宝支付配置
 */
public class AlipayConfig {
    // 应用ID,您的APPID，收款账号既是您的APPID对应支付宝账号
    public static String app_id = "2016091600524815";

    // 商户私钥，您的PKCS8格式RSA2私钥
    public static String merchant_private_key = "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCdfVeMO1PRWE5vdOhllq+0EUzfJJym8Bg75FrDoQjEixE8h5Xc1wY3XmMvkCPUOqGQcK4z78q5StB4LT6I2TDa56ZhklP14ttdEzo0cHnN8p9pNjt0YGYHDT3pd/clL+i9GlKEPXY3tN8Ij5fCN9rzUoDdpoknSlwxJ/44vfgT6bQlp7MWbv+tY0EVJG8iB6e8M0pv8OdPjq08Jgw7Fsr7A7e/j7+qYbEoRG3rRgZ/uo6p3Tn6GgRb1nPfBV23GYxw+tEyXO4sIjwDMKWxwe7HtJ4MLd49aoUhJRx9aW43E36K2z9/NARPYwByo8DVRdhOFMWOA+rR6MmrSPkx+JQjAgMBAAECggEAIQSiUjgt/nnxF9T+1C2fcLUf1LisTyOPMR9TGCiu2eX+Gx6iAMbj+r/DM7mYiWoxbULygtkHO4m/4zI5Jh/C6mIes94l1CtXqk/ZqBzcrJztZvWDyYZcXaYdENGh8x30QZE/M5JfMpatG/Je8s0bDmCBu/aqUp54baXg2qyZUjMcVkSU8qkhzXNdQ4aCEVmPdl3ixpQjzTrZnVKmIWH7k4twSRF7He+DHchjc5mXi6sHO0K0bsVZuOO8iAGVZF2TZfk2SesJ/RIpSVggPiJOzU7UznjMW4Cm5YDXl1grysRAmWkwlUF99Kr5vxfF+T5+rSca/qYlwrcgW47/nWIDYQKBgQDh5L7ujbC7qVDj/pv65wjlmbYexozv5UoFE2h0nvT4P0AG613bt6MQ+jH6T3CkoCk/nMXC4VnLMs6KC89HeCO9BYFo9QUjA5fWubzomIuBoK4PSPRAqNhiRVE4SOS2oA4IGSc9uHJd287SSv5ez+hKQWteKK4YZF6HnDMZ2nDffQKBgQCyermbVbphtDtNiFcDUyYX6qSmBrfp+Yi4s24oHfS3bZqhKzWdAmu7bsVLEPhtB2Q9kbapE6ZabpykhRFRrp7qjldrA2ko/Ffloappb+oX5pqacGVPZWBhyzaLcKqEtTQz72WRRQp6SpJYvuhJx987tCpCGYUjklcAM52Z80LUHwKBgQCx0we29VWGNWCXSoxxtEQdsqZajcTO6LofSsr021lOv0Pg7pHhcCtvJvYG7VhoUCiIihpoMkwkmOdcZrWStnGz0EyyWgfkK2TxRSAAHm3b6qh7Idwdto04twab/04EsfS5zUtF3Bgz6OBkTWL3MkXThrJF2lJKo2CC8qSLmpk2ZQKBgHf+5xc2tg7GfDCOf+HuX2gpC/XMAo6+hFuZ13AFY+iHOjUttegQHppvyRnFGSFEnPKAK0zVtzyJras3BAPk4VdVyBRcwLEbp4TuAoLNCZh0JHG9K4AL6pcVZ2CsqRh8M9LPG3xl7Lt3s5kTEV25ka60XM0AF3FpDDFIgqdk1AOFAoGBAMWdqWNr9n9gBOazP2goix118mrSBQ1d4I6hYLZQ0Iq9AnPePgAGPUJDgm3tGwI1xir79M1tjdSh97cowMNrqJrgRMY89YU2GgYuqYFcB7waIwbi4ZxB4GTHqOjnIV39we5IuKWmPAwSU9LupHupcXtwVaGGkayFF5GQ16oNxKGM";

    // 支付宝公钥,查看地址：https://openhome.alipay.com/platform/keyManage.htm 对应APPID下的支付宝公钥。
    public static String alipay_public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwPjI1P+lnvXKtqFcjKSUL8K6G7aoqRHD+kHrUn4iXIwjoNXarYbhX9DzDshd8yuNatUAGVFvCj63MbrNx3tnVOvyOolyk6sngvEbjig+VV/M3blM0rTvG8XFRx1yp6Bc4YlbbJt9n0GBOaoAuvEZWPFhCko77KjzMr0bGMF4Yff+d0IMJ1s3dYtL+Kj6SbRCXQwYeNDUeLrr4gBTaWhz71H5cneKL2GVTiy/XtkLQ1A0m4sIjnGqyLx78m2h2M9gRWK4wwQImpzsnrUgYfU0+ULzYmoE/FIAwYTZdlKUx/o17AH89gxmoSVqz3jz6PlSWrF3M3p/fPAHhsVdmvOt/QIDAQAB";

    // 服务器异步通知页面路径  需http://格式的完整路径，不能加?id=123这类自定义参数，必须外网可以正常访问
    public static String notify_url = "http://localhost:9090/butCart/success_pay.html";

    // 页面跳转同步通知页面路径 需http://格式的完整路径，不能加?id=123这类自定义参数，必须外网可以正常访问
    public static String return_url = "http://localhost:9090/butCart/success_pay.html";

    // 签名方式
    public static String sign_type = "RSA2";

    // 字符编码格式
    public static String charset = "utf-8";

    // 支付宝网关
    public static String gatewayUrl = "https://openapi.alipaydev.com/gateway.do";
}
