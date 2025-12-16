using System.Runtime.Serialization;

namespace ChatGateway.Contracts.Request;

public enum ChangeModelRequestEnumDto
{
    // GPT-5 family
    [EnumMember(Value = "gpt-5")]
    Gpt5,
    [EnumMember(Value = "gpt-5-mini")]
    Gpt5_Mini,
    [EnumMember(Value = "gpt-5-nano")]
    Gpt5_Nano,

    // GPT-4 family
    [EnumMember(Value = "gpt-4")]
    Gpt4,
    [EnumMember(Value = "gpt-4o")]
    Gpt4o,
    [EnumMember(Value = "gpt-4o-mini")]
    Gpt4o_Mini,

    // GPT-3.5 family
    [EnumMember(Value = "gpt-3.5-turbo")]
    Gpt3_5_Turbo,
    [EnumMember(Value = "gpt-3.5-turbo-0301")]
    Gpt3_5_Turbo_0301,
    [EnumMember(Value = "gpt-3.5-turbo-0613")]
    Gpt3_5_Turbo_0613,
    [EnumMember(Value = "gpt-3.5-turbo-16k")]
    Gpt3_5_Turbo_16k,
    [EnumMember(Value = "gpt-3.5-turbo-16k-0613")]
    Gpt3_5_Turbo_16k_0613,

}
