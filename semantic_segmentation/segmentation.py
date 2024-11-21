from dataloader import orig_train_batches, vald_batches, single_batch
from basemodel import model_net_MobileNetv2
from callback import savemodel_callback,DisplayCallback#,EarlyStopping_callback
from utils import checkpoint_filepath
import wandb
# Use wandb-core
wandb.require("core")
from wandb.integration.keras import WandbMetricsLogger


if __name__=="__main__":
        EPOCHS = 50
        model = model_net_MobileNetv2
        # model.load_weights(checkpoint_filepath)
        # Launch an experiment
        wandb.init(
            project="FL_segmentation",
            name= f"test",
            config={
                "epoch": EPOCHS
            },
        )
        config = wandb.config
        # Add WandbMetricsLogger to log metrics
        wandb_callbacks =WandbMetricsLogger()

        model_history = model.fit(single_batch,
                                  epochs=config.epoch,
                                  verbose = 0,
                                  validation_data=vald_batches,
                                  callbacks=[wandb_callbacks,savemodel_callback,DisplayCallback()]  #+EarlyStopping_callback
                                  )
        # Mark the run as finished
        wandb.finish()
