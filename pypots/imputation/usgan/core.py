"""
The implementation of USGAN for the partially-observed time-series imputation task.

Refer to the paper "Miao, X., Wu, Y., Wang, J., Gao, Y., Mao, X., & Yin, J. (2021).
Generative Semi-supervised Learning for Multivariate Time Series Imputation. AAAI 2021."

"""

# Created by Jun Wang <jwangfx@connect.ust.hk> and Wenjie Du <wenjay.du@gmail.com>
# License: BSD-3-Clause

import torch.nn as nn

from ...nn.modules.usgan import BackboneUSGAN


class _USGAN(nn.Module):
    """USGAN model"""

    def __init__(
        self,
        n_steps: int,
        n_features: int,
        rnn_hidden_size: int,
        lambda_mse: float,
        hint_rate: float = 0.7,
        dropout_rate: float = 0.0,
    ):
        super().__init__()
        self.backbone = BackboneUSGAN(
            n_steps,
            n_features,
            rnn_hidden_size,
            lambda_mse,
            hint_rate,
            dropout_rate,
        )

    def forward(
        self,
        inputs: dict,
        training_object: str = "generator",
        training: bool = True,
    ) -> dict:
        assert training_object in [
            "generator",
            "discriminator",
        ], 'training_object should be "generator" or "discriminator"'

        results = {}
        if training:
            if training_object == "discriminator":
                imputed_data, discrimination_loss = self.backbone(
                    inputs, training_object, training
                )
                loss = discrimination_loss
            else:
                imputed_data, generation_loss = self.backbone(
                    inputs,
                    training_object,
                    training,
                )
                loss = generation_loss
            results["loss"] = loss
        else:
            imputed_data = self.backbone(
                inputs,
                training_object,
                training,
            )

        results["imputed_data"] = imputed_data
        return results
