from typing import List, Dict, Any
from user import User


class RequestHandler:
    user_map = {}

    def __init__(self, request: Dict[str, Any]):
        self.request = request

    def handle_request(self) -> Dict[str, Any]:
        method_name: str = self.request.get("method_name")
        params: Dict[str, Any] = self.request.get("params")
        print("params:", params)
        param_types: List[str] = self.request.get("param_types")

        try:
            print("method_name:", method_name)
            converted_params = self.convert_params(params, param_types)
            print("converted_params:", converted_params)
            result = getattr(self, method_name)(**converted_params)
            print(self.user_map)
            return self.success_response(result)
        except Exception as e:
            return self.error_response(str(e))

    def register_user(self, user_name: str, address: str, port: int) -> bool:
        """
        ユーザーを登録する。
        ユーザー名でユーザーを識別する。
        ユーザー名が既に存在する場合はFalseを返す。
        ユーザー名が存在しない場合はTrueを返す。
        """
        if user_name in self.user_map:
            return False
        user = User(user_name=user_name, address=address, port=port)
        self.user_map[user_name] = user

        return True

    @staticmethod
    def convert_params(
        params: Dict[str, Any], param_types: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        パラメータを指定された型に変換します。

        Args:
            params (Dict[str, Any]): 変換するパラメータの辞書。
            param_types (Dict[str, str]): 各パラメータの型を示す文字列の辞書。

        Returns:
            Dict[str, Any]: 変換されたパラメータの辞書。

        Raises:
            ValueError: サポートされていない型が指定された場合、または変換に失敗した場合。
        """
        type_conversion_map = {
            "int": int,
            "float": float,
            "str": str,
            "bool": bool,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
        }

        converted_params = {}
        for param_name in params:
            try:
                # param: "1", param_type: int --> 1
                # param: "1.1", param_type: float --> 1.1
                # param: "hello", param_type: str --> "hello"
                # param: "[1, 2, 3]", param_type: list --> [1, 2, 3]
                param_type = param_types[param_name]
                param_value = params[param_name]
                converted_param = type_conversion_map[param_type](param_value)
                converted_params[param_name] = converted_param
            except Exception as e:
                raise e
        return converted_params

    @staticmethod
    def success_response(result: Any) -> Dict[str, Any]:
        result_type = type(result).__name__
        return {
            "result": "success",
            "message": result,
            "result_type": result_type,
        }

    @staticmethod
    def error_response(error: str) -> Dict[str, Any]:
        return {"result": "error", "message": error}
